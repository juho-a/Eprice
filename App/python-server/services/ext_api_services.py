from datetime import datetime, timezone
import httpx
from urllib.parse import urlencode
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import os

# Define a model for Fingrid data
class FingridData(BaseModel):
    startTime: str
    endTime: str
    value: float  # Replace this with the actual field name from Fingrid's API

# Define a model for error responses
class ErrorResponse(BaseModel):
    error: str



load_dotenv(dotenv_path="./.env.local")
FINGRID_API_KEY = os.getenv("FINGRID_API_KEY")

async def fetch_fingrid_data(dataset_id: int) -> FingridData | ErrorResponse:
    """
    Fetches a Fingrid dataset and removes the datasetId field from the results.

    Args:
        dataset_id (int): The ID of the Fingrid dataset (e.g., 165 or 245)

    Returns:
        FingridData: A single data point closest to the current time.
        ErrorResponse: An error message if the fetch fails.
    """
    url = f"https://data.fingrid.fi/api/datasets/{dataset_id}/data"
    headers = {"x-api-key": FINGRID_API_KEY}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            full_data = response.json()
            data = full_data.get("data", [])

            if not data:
                return ErrorResponse(error="No data available from Fingrid API")

            now = datetime.now(timezone.utc)

            # Find the data point closest to the current time
            def time_diff(item):
                start = datetime.fromisoformat(item["startTime"].replace("Z", "+00:00"))
                end = datetime.fromisoformat(item["endTime"].replace("Z", "+00:00"))
                return min(abs(start - now), abs(end - now))

            closest_item = min(data, key=time_diff)
            closest_item.pop("datasetId", None)
            return FingridData(**closest_item)

    except Exception as e:
        return ErrorResponse(error=f"Failed to fetch data for dataset {dataset_id} from Fingrid API with error: {str(e)}")


async def fetch_weather_data(lat: float, lon: float, requested_dt: datetime) -> dict:
    """
    Fetches the weather forecast and returns the closest moment's temperature and wind speed.

    Args:
        lat (float): Latitude
        lon (float): Longitude
        requested_dt (datetime): UTC timestamp for which the closest forecast is fetched

    Returns:
        dict: Temperature, wind speed, and forecast timestamp or an error message
    """
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    headers = {
        "User-Agent": "eprice-app"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        timeseries = data.get("properties", {}).get("timeseries", [])
        if not timeseries:
            return {"error": "No timeseries data available"}

        closest_entry = min(
            timeseries,
            key=lambda x: abs(datetime.fromisoformat(x["time"].replace("Z", "+00:00")) - requested_dt)
        )

        details = closest_entry.get("data", {}).get("instant", {}).get("details", {})
        return {
            "temperature_celsius": details.get("air_temperature"),
            "wind_speed_mps": details.get("wind_speed"),
            "closest_forecast_time": closest_entry.get("time")
        }

    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}"}
    except Exception as e:
        return {"error": f"Unexpected error occurred: {str(e)}"}
    
async def fetch_fingrid_data_range(dataset_id: int, start_time: str, end_time: str) -> List[FingridData] | ErrorResponse:
    """
    Fetches Fingrid dataset data for a given time interval and removes the datasetId field.

    Args:
        dataset_id (int): Fingrid dataset ID.
        start_time (str): ISO 8601 formatted start time.
        end_time (str): ISO 8601 formatted end time.

    Returns:
        List[FingridData]: A list of data points for the given time range.
        ErrorResponse: An error message if the fetch fails.
    """
    base_url = f"https://data.fingrid.fi/api/datasets/{dataset_id}/data"
    headers = {"x-api-key": FINGRID_API_KEY}
    
    query_params = {
        "startTime": start_time,
        "endTime": end_time,
        "sortBy": "startTime",
        "sortOrder": "asc",
        "pageSize": "20000"
    }

    url = f"{base_url}?{urlencode(query_params)}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            full_data = response.json()
            data = full_data.get("data", [])
            for item in data:
                item.pop("datasetId", None)
            return [FingridData(**item) for item in data]
    except Exception as e:
        return ErrorResponse(error=f"Failed to fetch data for dataset {dataset_id} from Fingrid API: {str(e)}")
