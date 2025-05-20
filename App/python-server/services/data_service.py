from models.data_model import *
from ext_apis.ext_apis import *
from repositories.porssisahko_repository import *
from config.secrets import DATABASE_URL
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo



class FingridDataService:
    def __init__(self):
        self.ext_api_fetcher = FetchFingridData()

    async def fingrid_data(self, dataset_id: int) -> FingridDataPoint | ErrorResponse:
        return await self.ext_api_fetcher.fetch_fingrid_data(dataset_id)
    
    async def fingrid_data_range(self, dataset_id: int, start_time: str, end_time: str) -> List[FingridDataPoint] | ErrorResponse:
        return await self.ext_api_fetcher.fetch_fingrid_data_range(dataset_id,start_time, end_time)


class PriceDataService:
    def __init__(self):
        self.ext_api_fetcher = FetchPriceData()
        self.database_fetcher = PorssisahkoRepository(DATABASE_URL)

    async def price_data_latest(self) -> List[PriceDataPoint]:
        now_aware = datetime.now(timezone.utc)
        helsinki_tz = ZoneInfo("Europe/Helsinki")
        #now_aware = datetime.now(helsinki_tz)
        start_date = (now_aware - timedelta(hours=48)).replace(tzinfo=None)
        end_date = now_aware.replace(tzinfo=None)
        start_date = datetime(2025, 5, 19, 15, 0, 0)
        end_date = datetime(2025, 5, 20, 23, 0, 0)



        print("start_date", start_date)
        print("end_date", end_date)
        print("now_aware", now_aware)
        try:
            sample = await self.database_fetcher.get_entries(
                start_date=start_date,
                end_date=end_date,
                select_columns="datetime, price"
            )
            result = []
            for item in sample:
                print("item", item)
                # Muunna Helsingin ajasta UTC:ksi
                helsinki_time = item["datetime"]
                utc_time = helsinki_time.astimezone(ZoneInfo("UTC"))
                result.append(
                    PriceDataPoint(
                        startDate=utc_time,
                        price=item["price"]
                    )
                )
            print(len(result), "result")
            return result
        except Exception as e:
            # If database fetch fails, fall back to external API
            return await self.ext_api_fetcher.fetch_price_data_latest()
    
    async def price_data_today(self) -> List[PriceDataPoint]:
     
        return await self.ext_api_fetcher.fetch_price_data_today()
    
    async def price_data_range(self, start_time: datetime, end_time: datetime) -> List[PriceDataPoint]:
        return await self.ext_api_fetcher.fetch_price_data_range(start_time, end_time)