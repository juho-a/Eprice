from models.data_model import *
from ext_api_fetcher.ext_api_fetcher import *


class FingridDataService:
    def __init__(self):
        self.fetcher = FetchFingridData()

    async def fingrid_data(self, dataset_id: int) -> FingridDataPoint | ErrorResponse:
        return await self.fetcher.fetch_fingrid_data(dataset_id)
    
    async def fingrid_data_range(self, dataset_id: int, start_time: str, end_time: str) -> List[FingridDataPoint] | ErrorResponse:
        return await self.fetcher.fetch_fingrid_data_range(dataset_id,start_time, end_time)


class WeatherDataService:
    def __init__(self):
        self.fetcher = FetchWeatherData()

    async def weather_data(self, lat: float, lon: float, requested_dt: str) -> WeatherDataPoint | ErrorResponse:
        return await self.fetcher.fetch_weather_data(lat, lon, requested_dt)


class PriceDataService:
    def __init__(self):
        self.fetcher = FetchPriceData()

    async def price_data_latest(self) -> List[PriceDataPoint]:
        return await self.fetcher.fetch_price_data_latest()
    
    async def price_data_today(self) -> List[PriceDataPoint]:
        return await self.fetcher.fetch_price_data_today()
    
    async def price_data_range(self, start_time: str, end_time: str) -> List[PriceDataPoint]:
        return await self.fetcher.fetch_price_data_range(start_time, end_time)