from datetime import datetime
from models.data_model import *
from ext_api.ext_api import *


class FingridDataService:
    def __init__(self):
        self.fetcher = FetchFingridData()

    async def fingrid_data(self, dataset_id: int):
        return await self.fetcher.fetch_fingrid_data(dataset_id)
    
    async def fingrid_data_range(self, dataset_id: int, start_time: str, end_time: str):
        return await self.fetcher.fetch_fingrid_data_range(dataset_id,start_time, end_time)


class WeatherdDataService:
    def __init__(self):
        self.fetcher = FetchWeatherData()

    async def weather_data(self, lat: float, lon: float, requested_dt: datetime):
        return await self.fetcher.fetch_weather_data(lat, lon, requested_dt)



class PriceDataService:
    def __init__(self):
        self.fetcher = FetchPriceData()

    async def price_data_latest(self):
        return await self.fetcher.fetch_price_data_latest()
    
    async def price_data_today(self):
        return await self.fetcher.fetch_price_data_today()
    
    async def price_data_range(self, start_time: str, end_time: str):
        return await self.fetcher.fetch_price_data_range(start_time, end_time)


