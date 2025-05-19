from models.data_model import *
from ext_apis.ext_apis import *



class FingridDataService:
    def __init__(self):
        self.fetcher = FetchFingridData()

    async def fingrid_data(self, dataset_id: int) -> FingridDataPoint | ErrorResponse:
        return await self.fetcher.fetch_fingrid_data(dataset_id)
    
    async def fingrid_data_range(self, dataset_id: int, start_time: str, end_time: str) -> List[FingridDataPoint] | ErrorResponse:
        return await self.fetcher.fetch_fingrid_data_range(dataset_id,start_time, end_time)


class PriceDataService:
    def __init__(self):
        self.fetcher = FetchPriceData()

    async def price_data_latest(self) -> List[PriceDataPoint]:
        return await self.fetcher.fetch_price_data_latest()
    
    async def price_data_today(self) -> List[PriceDataPoint]:
        return await self.fetcher.fetch_price_data_today()
    
    async def price_data_range(self, start_time: datetime, end_time: datetime) -> List[PriceDataPoint]:
        return await self.fetcher.fetch_price_data_range(start_time, end_time)