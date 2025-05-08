from fastapi import APIRouter, Query
from datetime import datetime, timezone
from services.ext_api_services import fetch_fingrid_data, fetch_weather_data, fetch_fingrid_data_range
from pydantic import BaseModel
import httpx


class TimeRangeRequest(BaseModel):
    startTime: str  # RFC 3339 format
    endTime: str    # RFC 3339 format


router = APIRouter()


# windpower
@router.get("/api/public/windpower")
async def get_windpower():
    """
    Returns the wind power production forecast from the Fingrid API.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data(dataset_id=245)

@router.post("/api/public/windpower/range")
async def post_windpower_range(time_range: TimeRangeRequest):
    """
    Returns wind power production data from Fingrid API for a given time range via POST method.

    Args:
        time_range (TimeRangeRequest): Contains startTime and endTime in RFC 3339 format.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data_range(
        dataset_id=245,
        start_time=time_range.startTime,
        end_time=time_range.endTime
    )

# consumption
@router.get("/api/public/consumption")
async def get_consumption():
    """
    Returns the consumption forecast from the Fingrid API.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data(dataset_id=165)


@router.post("/api/public/consumption/range")
async def post_windpower_range(time_range: TimeRangeRequest):
    """
    Returns consumption data from Fingrid API for a given time range via POST method.

    Args:
        time_range (TimeRangeRequest): Contains startTime and endTime in RFC 3339 format.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data_range(
        dataset_id=165,
        start_time=time_range.startTime,
        end_time=time_range.endTime
    )

# production
@router.get("/api/public/production")
async def get_consumption():
    """
    Returns the consumption forecast from the Fingrid API.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data(dataset_id=241)



@router.post("/api/public/production/range")
async def post_windpower_range(time_range: TimeRangeRequest):
    """
    Returns production data from Fingrid API for a given time range via POST method.

    Args:
        time_range (TimeRangeRequest): Contains startTime and endTime in RFC 3339 format.

    Returns:
        list[dict] | dict: A list of data points or an error message.
    """
    return await fetch_fingrid_data_range(
        dataset_id=241,
        start_time=time_range.startTime,
        end_time=time_range.endTime
    )


# price data
@router.get("/api/public/data")
async def get_prices():
    """
    Fetch the latest prices from the external API and extract prices and hours.

    Returns:
        dict: A dictionary with keys 'values' (prices) and 'labels' (hours).
    """
    url = "https://api.porssisahko.net/v1/latest-prices.json"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()  # Parse the JSON response

            # Extract prices and hours
            prices = [item["price"] for item in data["prices"]]
            hours = [item["startDate"][11:16] for item in data["prices"]]  # Extract hour (HH:MM) from startDate
            assert len(prices) == len(hours), "Prices and hours lists must be of the same length"
            
            # sort the prices and hours by hour
            prices, hours = zip(*sorted(zip(prices, hours), key=lambda x: x[1]))
            
            # Convert prices to float
            prices = [float(price) for price in prices]
            # take every 2nd element
            prices = prices[::2]
            # Convert hours to string
            hours = list(range(24))#[str(hour) for hour in hours]
            
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
    
# Weather
@router.get("/api/public/weather")
async def get_weather(lat: float, lon: float, timestamp: str = Query(..., description="UTC datetime in RFC 3339 form, e.g. 2024-05-05T13:30:00Z")):
    """
    Returns the weather forecast for a selected UTC timestamp.

    Args:
        lat (float): Latitude
        lon (float): Longitude
        timestamp (str): UTC datetime in RFC 3339 format (e.g., 2024-05-05T13:30:00Z)

    Returns:
        dict: Weather information or an error message
    """
    try:
        requested_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
        return await fetch_weather_data(lat, lon, requested_dt)
    except ValueError:
        return {"error": "Invalid timestamp format. Expected RFC 3339 format (e.g. 2024-05-05T13:30:00Z)"}