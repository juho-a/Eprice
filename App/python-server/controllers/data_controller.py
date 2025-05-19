from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from typing import List
from services.data_service import FingridDataService, PriceDataService, WeatherDataService
from models.data_model import FingridDataPoint, TimeRangeRequest, WeatherRequest, WeatherDataPoint, PriceDataPoint, ErrorResponse
from fastapi import HTTPException

router = APIRouter()
fingrid_data_service = FingridDataService()
price_data_service = PriceDataService()
weather_data_service = WeatherDataService()


@router.get("/api/public/windpower", response_model=FingridDataPoint, responses={500: {"model": ErrorResponse, "description": "Internal server error"}})

async def get_windpower():
    """
    Get wind power production forecast.
    Fetches forecast data from Fingrid dataset ID 245.

    Returns:
        dict: A data point or an error message.
    """
    try:
        return await fingrid_data_service.fingrid_data(dataset_id=245)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "status_code": 500})


@router.post("/api/public/windpower/range", response_model=List[FingridDataPoint],
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}})

async def post_windpower_range(time_range: TimeRangeRequest):
    """
    Get wind power production data for a given time range.
    Fetches data from Fingrid dataset ID 245.

    Args:
        time_range (TimeRangeRequest): Start and end time in RFC 3339 format.

    Returns:
        list[dict]: A list of data points or an error message.
    """
    try:
        return await fingrid_data_service.fingrid_data_range(
            dataset_id=245,
            start_time=time_range.startTime,
            end_time=time_range.endTime)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "status_code": 500})


@router.get("/api/public/consumption",
    response_model=FingridDataPoint,
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}})

async def get_consumption():
    """
    Get electricity consumption forecast.
    Fetches consumption data from Fingrid dataset ID 165.

    Returns:
        dict: A data point or an error message.
    """
    try:
        return await fingrid_data_service.fingrid_data(dataset_id=165)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "status_code": 500})


@router.post("/api/public/consumption/range", response_model=List[FingridDataPoint],
             responses={500: {"model": ErrorResponse, "description": "Internal server error"}})

async def post_consumption_range(time_range: TimeRangeRequest):
    """
    Get electricity consumption data for a given time range.
    Fetches consumption data from Fingrid dataset ID 165.

    Args:
        time_range (TimeRangeRequest): Start and end time in RFC 3339 format.

    Returns:
        list[dict]: A list of data points or an error message.
    """
    try:
        return await fingrid_data_service.fingrid_data_range(
            dataset_id=165,
            start_time=time_range.startTime,
            end_time=time_range.endTime
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "status_code": 500})


@router.get("/api/public/production",
    response_model=FingridDataPoint,
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}})

async def get_production():
    """
    Get electricity production forecast.
    Fetches production data from Fingrid dataset ID 241.

    Returns:
        dict: A data point or an error message.
    """
    try:
        return await fingrid_data_service.fingrid_data(dataset_id=241)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "status_code": 500})

@router.post("/api/public/production/range", response_model=List[FingridDataPoint],
            responses={500: {"model": ErrorResponse, "description": "Internal server error"}})

async def post_production_range(time_range: TimeRangeRequest):
    """
    Get electricity production data for a given time range.
    Fetches production data from Fingrid dataset ID 241.

    Args:
        time_range (TimeRangeRequest): Start and end time in RFC 3339 format.

    Returns:
        list[dict]: A list of data points or an error message.
    """
    try:
        return await fingrid_data_service.fingrid_data_range(
            dataset_id=241,
            start_time=time_range.startTime,
            end_time=time_range.endTime
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "status_code": 500})

@router.post("/api/public/weather", response_model=WeatherDataPoint)
async def post_weather(request: WeatherRequest):
    """
    Get weather forecast for a specific UTC time and location (POST version).
    Fetches weather forecast data from the MET API.

    Args:
        request (WeatherRequest): Contains latitude, longitude, and timestamp in RFC 3339 format.

    Returns:
        dict: Weather forecast data or an error message.
    """
    try:
        requested_dt = datetime.fromisoformat(request.timestamp.replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
        return await weather_data_service.weather_data(request.lat, request.lon, requested_dt)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "status_code": 500})

@router.post("/api/public/price/range")
async def post_price_range(time_range: TimeRangeRequest):
    """
    Get price data for specific time range from Porssisahko API
    """
    try:
        return await price_data_service.price_data_range(
            time_range.startTime, time_range.endTime
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "status_code": 500})


@router.get(
    "/api/public/data",
    response_model=List[PriceDataPoint],
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}})
async def get_prices():
    try:
        return await price_data_service.price_data_latest()
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "status_code": 500})

@router.get(
    "/api/public/data/today",
    response_model=List[PriceDataPoint],
    responses={500: {"model": ErrorResponse, "description": "Internal server error"}})
async def get_prices_today():
    try:
        return await price_data_service.price_data_today()
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail, "status_code": e.status_code})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "status_code": 500})