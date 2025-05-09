from fastapi import APIRouter, Query
from datetime import datetime, timezone
from services.ext_api_services import fetch_fingrid_data, fetch_weather_data, fetch_fingrid_data_range
from pydantic import BaseModel, Field, RootModel
from typing import List
import httpx


class TimeRangeRequest(BaseModel):
    startTime: str = Field(
        example="2024-05-01T00:00:00Z",
        description="Start time in RFC 3339 format (e.g., 2024-05-01T00:00:00Z)"
    )
    endTime: str = Field(
        example="2024-05-02T00:00:00Z",
        description="End time in RFC 3339 format (e.g., 2024-05-02T00:00:00Z)"
    )

class DataPoint(BaseModel):
    startTime: str = Field(..., example="2025-05-08T04:00:00.000Z")
    endTime: str = Field(..., example="2025-05-08T04:15:00.000Z")
    value: float = Field(..., example=7883.61)


class DataResponse(RootModel[List[DataPoint]]):
    pass


router = APIRouter()


@router.get("/api/public/windpower", response_model=RootModel[DataPoint])
async def get_windpower():
    """
    Get wind power production forecast.
    Fetches forecast data from Fingrid dataset ID 245.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data(dataset_id=245)


@router.post("/api/public/windpower/range", response_model=RootModel[List[DataPoint]])
async def post_windpower_range(time_range: TimeRangeRequest):
    """
    Get wind power production data for a given time range.
    Fetches data from Fingrid dataset ID 245.

    Args:
        time_range (TimeRangeRequest): Start and end time in RFC 3339 format.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data_range(
        dataset_id=245,
        start_time=time_range.startTime,
        end_time=time_range.endTime
    )


@router.get("/api/public/consumption", response_model=RootModel[DataPoint])
async def get_consumption():
    """
    Get electricity consumption forecast.
    Fetches consumption data from Fingrid dataset ID 165.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data(dataset_id=165)


@router.post("/api/public/consumption/range", response_model=RootModel[List[DataPoint]])
async def post_consumption_range(time_range: TimeRangeRequest):
    """
    Get electricity consumption data for a given time range.
    Fetches consumption data from Fingrid dataset ID 165.

    Args:
        time_range (TimeRangeRequest): Start and end time in RFC 3339 format.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data_range(
        dataset_id=165,
        start_time=time_range.startTime,
        end_time=time_range.endTime
    )


@router.get("/api/public/production", response_model=RootModel[DataPoint])
async def get_production():
    """
    Get electricity production forecast.
    Fetches production data from Fingrid dataset ID 241.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data(dataset_id=241)


@router.post("/api/public/production/range", response_model=RootModel[List[DataPoint]])
async def post_production_range(time_range: TimeRangeRequest):
    """
    Get electricity production data for a given time range.
    Fetches production data from Fingrid dataset ID 241.

    Args:
        time_range (TimeRangeRequest): Start and end time in RFC 3339 format.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data_range(
        dataset_id=241,
        start_time=time_range.startTime,
        end_time=time_range.endTime
    )


@router.get("/api/public/data", response_model=RootModel[DataPoint])
async def get_prices():
    """
    Get hourly electricity prices from external API.

    Fetches latest hourly prices and formats them for charting.

    Returns:
        dict: Contains chart legend, type, values (snt/kWh), labels (hours), and status message.
    """
    url = "https://api.porssisahko.net/v1/latest-prices.json"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            prices = [item["price"] for item in data["prices"]]
            hours = [item["startDate"][11:16] for item in data["prices"]]
            assert len(prices) == len(hours), "Prices and hours lists must be of the same length"

            prices, hours = zip(*sorted(zip(prices, hours), key=lambda x: x[1]))
            prices = [float(price) for price in prices][::2]
            hours = list(range(24))

            return {
                "chartLegend": "Prices (snt / kWh)",
                "chartType": "bar",
                "chartValues": prices,
                "chartLabels": hours,
                "message": "Prices fetched successfully"
            }
    except httpx.RequestError as exc:
        return {"error": f"An error occurred while requesting {exc.request.url}: {str(exc)}"}
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}"}


@router.get("/api/public/weather")
async def get_weather(
    lat: float,
    lon: float,
    timestamp: str = Query(..., description="UTC datetime in RFC 3339 format, e.g. 2024-05-05T13:30:00Z")
):
    """
    Get weather forecast for a specific UTC time and location.
    Fetches weather forecast data from the MET API.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.
        timestamp (str): UTC datetime in RFC 3339 format (e.g., 2024-05-05T13:30:00Z).

    Returns:
        dict: Weather forecast data or an error message.
    """
    try:
        requested_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
        return await fetch_weather_data(lat, lon, requested_dt)
    except ValueError:
        return {"error": "Invalid timestamp format. Expected RFC 3339 format (e.g. 2024-05-05T13:30:00Z)"}