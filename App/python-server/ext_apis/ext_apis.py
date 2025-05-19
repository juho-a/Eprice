from datetime import datetime, timezone, timedelta
import httpx
from urllib.parse import urlencode
from typing import List
from dotenv import load_dotenv
import os
from models.data_model import *
from zoneinfo import ZoneInfo
from models.data_model import PriceDataPoint
from fastapi import HTTPException
import asyncio


load_dotenv(dotenv_path="./.env.local")
FINGRID_API_KEY = os.getenv("FINGRID_API_KEY")



class FetchFingridData:
    base_url = "https://data.fingrid.fi/api/datasets/"

    def __init__(self):
        self._lock = asyncio.Lock()
        self._last_call_time: datetime | None = None
        self._sleep_time = 1.5

    async def _rate_limiter(self):
        async with self._lock:
            if self._last_call_time:
                elapsed = (datetime.now(timezone.utc)- self._last_call_time).total_seconds()
                if elapsed < self._sleep_time:
                    await asyncio.sleep(self._sleep_time - elapsed)
            self._last_call_time = datetime.now(timezone.utc)

    async def fetch_fingrid_data(self, dataset_id: int) -> FingridDataPoint:
        await self._rate_limiter() 
        url = f"{self.base_url}{dataset_id}/data"
        headers = {"x-api-key": FINGRID_API_KEY}
        max_retries = 3
        retry_delay = 3

        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=headers)
                    response.raise_for_status()
                    full_data = response.json()
                    data = full_data.get("data", [])

                    if not data:
                        raise ValueError("No data available from Fingrid API")

                    now = datetime.now(timezone.utc)

                    def time_diff(item):
                        start = datetime.fromisoformat(item["startTime"].replace("Z", "+00:00"))
                        end = datetime.fromisoformat(item["endTime"].replace("Z", "+00:00"))
                        return min(abs(start - now), abs(end - now))

                    closest_item = min(data, key=time_diff)
                    closest_item.pop("datasetId", None)
                    return FingridDataPoint(**closest_item)

            except httpx.HTTPStatusError as exc:
                if attempt == max_retries - 1:
                    raise HTTPException(
                        status_code=exc.response.status_code,
                        detail=f"HTTP error while fetching data for dataset {dataset_id} from Fingrid API with error message: {str(exc)} Number of attempts: {attempt +1}"
                    ) from exc
                await asyncio.sleep(retry_delay)

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error fetching data for dataset {dataset_id} from Fingrid API: {str(e)}"
                ) from e
        

    async def fetch_fingrid_data_range(self, dataset_id: int, start_time: str, end_time: str) -> List[FingridDataPoint] | ErrorResponse:
        await self._rate_limiter() 
        url = f"{self.base_url}{dataset_id}/data"
        headers = {"x-api-key": FINGRID_API_KEY}
        max_retries = 3
        retry_delay = 1

       
        query_params = {
            "startTime": start_time,
            "endTime": end_time,
            "sortBy": "startTime",
            "sortOrder": "asc",
            "pageSize": "20000"
        }

        url = f"{url}?{urlencode(query_params)}"
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=headers)
                    response.raise_for_status()
                    full_data = response.json()
                    data = full_data.get("data", [])
                    for item in data:
                        item.pop("datasetId", None)
                    return [FingridDataPoint(**item) for item in data]
            except httpx.HTTPStatusError as exc:
                if attempt == max_retries - 1:
                    raise HTTPException(
                        status_code=exc.response.status_code,
                        detail=f"HTTP error while fetching data for dataset {dataset_id} from Fingrid API with error message: {str(exc)}. Number of attempts: {attempt +1}"
                    ) from exc
                await asyncio.sleep(retry_delay)

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error fetching data for dataset {dataset_id} from Fingrid API: {str(e)}"
                ) from e
        


class FetchWeatherData:
    async def fetch_weather_data(self, lat: float, lon: float, requested_dt: datetime) -> dict:
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
                raise ValueError("No timeseries data available from weather API")

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
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"HTTP error while fetching data from met.no: {exc.response.status_code}: {exc.response.text}"
            ) from exc
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error occurred while fetching weather data: {str(e)}"
            ) from e


class FetchPriceData:
    base_url = "https://api.porssisahko.net/v1/price.json"

    async def fetch_price_data_range(self, start_time: str, end_time: str):
        start_datetime = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        end_datetime = datetime.fromisoformat(end_time.replace("Z", "+00:00"))

        result = []
        current_datetime = start_datetime

        while current_datetime <= end_datetime:
            date_str = current_datetime.strftime("%Y-%m-%d")
            hour_str = current_datetime.strftime("%H")

            query_params = {
                "date": date_str,
                "hour": hour_str
            }

            url = f"{self.base_url}?{urlencode(query_params)}"
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url)
                    response.raise_for_status()

                    data = response.json()
                    if not data:
                        raise ValueError(f"No price data returned for {date_str} {hour_str}")

                    result.append({
                        "startDate": f"{date_str}T{hour_str}:00:00Z",
                        "price": data["price"]
                    })
            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=f"HTTP error while fetching price data from Porssisahko: {exc.response.status_code}: {exc.response.text}"
                ) from exc
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error occurred while fetching data from Porssisahko: {str(e)}"
                ) from e

            current_datetime += timedelta(hours=1)

        return result


    async def fetch_price_data_latest(self):
        """
        Fetches the latest hourly electricity prices from the API.

        Returns the prices as a list with the 'endDate' field removed from each entry.

        Returns:
            list: A list of PriceDataPoint instances containing hourly electricity price data.
                  The 'endDate' key is removed from each dictionary.
        """
        url = "https://api.porssisahko.net/v1/latest-prices.json"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()["prices"]

                for item in data:
                    item.pop("endDate", None)

                return [PriceDataPoint(**item) for item in data]

        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"HTTP error while fetching latest price data from Porssisahko: {exc.response.status_code} - {exc.response.text}"
            ) from exc
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error while fetching latest price data from Porssisahko: {str(e)}"
            ) from e



    async def fetch_price_data_today(self) -> List[PriceDataPoint]:
        """
        Fetches today's electricity price data and returns it as a list of PriceDataPoint models.

        Returns:
            List[PriceDataPoint]: A list of price data points for today.
        """
        data = await self.fetch_price_data_latest()

        # Get the current date in Finland's timezone
        now_fi = datetime.now(ZoneInfo("Europe/Helsinki"))
        today_fi = now_fi.date()

        # Filter data for today's date
        filtered_data = [
            item for item in data
            if datetime.fromisoformat(item.startDate.replace("Z", "+00:00"))
            .astimezone(ZoneInfo("Europe/Helsinki"))
            .date() == today_fi
        ]

        # Convert filtered data to PriceDataPoint models
        return [PriceDataPoint(**item.dict()) for item in filtered_data]
