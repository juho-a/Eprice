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
        headers = {}
        if FINGRID_API_KEY is not None:
            headers["x-api-key"] = FINGRID_API_KEY
        max_retries = 3
        retry_delay = 3

        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    # Remove any None values from headers to satisfy type checker
                    clean_headers = {k: v for k, v in headers.items() if v is not None}
                    response = await client.get(url, headers=clean_headers)
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
                        detail=f"HTTP error while fetching data for dataset {dataset_id} from Fingrid API. Number of attempts: {attempt +1}"
                    ) from exc
                await asyncio.sleep(retry_delay)

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error fetching data for dataset {dataset_id} from Fingrid API."
                ) from e
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch data for dataset {dataset_id} from Fingrid API after {max_retries} attempts."
        )
        

    async def fetch_fingrid_data_range(self, dataset_id: int, start_time: datetime, end_time: datetime) -> List[FingridDataPoint]:
        headers = {"x-api-key": FINGRID_API_KEY} if FINGRID_API_KEY is not None else {}
        # Remove any None values from headers to satisfy type checker
        headers = {k: v for k, v in headers.items() if v is not None}
        url = f"{self.base_url}{dataset_id}/data"
        max_retries = 3
        retry_delay = 1

            
        query_params = {
            "startTime": start_time.isoformat().replace("+00:00", "Z"),
            "endTime": end_time.isoformat().replace("+00:00", "Z"),
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
                        detail=f"HTTP error while fetching data for dataset {dataset_id} from Fingrid API. Number of attempts: {attempt +1}"
                    ) from exc
                await asyncio.sleep(retry_delay)

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error fetching data for dataset {dataset_id} from Fingrid API."
                ) from e
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch data for dataset {dataset_id} from Fingrid API after {max_retries} attempts."
        )

class FetchPriceData:
    base_url = "https://api.porssisahko.net/v1/price.json"

    async def fetch_price_data_range(self, start_time: datetime, end_time: datetime):

        result = []
        current_time_utc = start_time
        current_time_helsinki = start_time.astimezone(ZoneInfo("Europe/Helsinki"))

        while current_time_helsinki <= end_time:
            date_str = current_time_helsinki.strftime("%Y-%m-%d")
            hour_str = current_time_helsinki.strftime("%H")

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
                        "startDate": current_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
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

            current_time_helsinki += timedelta(hours=1)
            current_time_utc += timedelta(hours=1)

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
        
        filtered_data = [item for item in data if item.startDate.astimezone(ZoneInfo("Europe/Helsinki")).date() == today_fi]

        # Convert filtered data to PriceDataPoint models
        return [PriceDataPoint(**item.dict()) for item in filtered_data]
