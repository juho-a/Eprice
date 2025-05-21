from models.data_model import *
from ext_apis.ext_apis import *
from repositories.porssisahko_repository import *
from utils.porssisahko_service_tools import *
from config.secrets import DATABASE_URL
from datetime import datetime
from zoneinfo import ZoneInfo

class FingridDataService:
    """
    Service class for fetching Fingrid data from the external API.
    """

    def __init__(self):
        """
        Initialize the FingridDataService with the external API fetcher.
        """
        self.ext_api_fetcher = FetchFingridData()

    async def fingrid_data(self, dataset_id: int) -> FingridDataPoint | ErrorResponse:
        """
        Fetch the latest Fingrid data for a given dataset ID.

        Args:
            dataset_id (int): The Fingrid dataset ID.

        Returns:
            FingridDataPoint | ErrorResponse: The latest data point or an error response.
        """
        return await self.ext_api_fetcher.fetch_fingrid_data(dataset_id)
    
    async def fingrid_data_range(self, dataset_id: int, start_time: str, end_time: str) -> List[FingridDataPoint] | ErrorResponse:
        """
        Fetch Fingrid data for a given dataset ID and time range.

        Args:
            dataset_id (int): The Fingrid dataset ID.
            start_time (str): Start time in ISO format.
            end_time (str): End time in ISO format.

        Returns:
            List[FingridDataPoint] | ErrorResponse: List of data points or an error response.
        """
        return await self.ext_api_fetcher.fetch_fingrid_data_range(dataset_id, start_time, end_time)


class PriceDataService:
    """
    Service class for handling price data operations, including fetching from the database and external API.
    """

    def __init__(self):
        """
        Initialize the PriceDataService with required repositories and helper services.
        """
        self.ext_api_fetcher = FetchPriceData()
        self.database_fetcher = PorssisahkoRepository(DATABASE_URL)
        self.porssisahko_service_tools = PorssisahkoServiceTools(self.ext_api_fetcher, self.database_fetcher)

    async def price_data_latest(self) -> List[PriceDataPoint]:
        """
        Fetch the latest 48 hours of price data, preferring the database but falling back to the external API if needed.

        Returns:
            List[PriceDataPoint]: List of price data points for the latest 48 hours.
        """
        start_date, end_date = self.porssisahko_service_tools.expected_time_range()
        try:
            result = await self.porssisahko_service_tools.fetch_and_process_data(start_date, end_date)
            return result if result else await self.ext_api_fetcher.fetch_price_data_latest()
        except Exception:
            return await self.ext_api_fetcher.fetch_price_data_latest()

    async def price_data_range(self, start_date: datetime, end_date: datetime) -> List[PriceDataPoint]:
        """
        Fetch price data for a given time range, preferring the database but falling back to the external API if needed.

        Args:
            start_date (datetime): Start of the time range.
            end_date (datetime): End of the time range.

        Returns:
            List[PriceDataPoint]: List of price data points for the given range.
        """
        start_date = start_date.replace(tzinfo=None)
        end_date = end_date.replace(tzinfo=None)
        try:
            result = await self.porssisahko_service_tools.fetch_and_process_data(start_date, end_date)
            return result if result else await self.ext_api_fetcher.fetch_price_data_range(start_date, end_date)
        except Exception:
            return await self.ext_api_fetcher.fetch_price_data_range(start_date, end_date)

    async def price_data_today(self) -> List[PriceDataPoint]:
        """
        Fetch price data for the current day in Helsinki time.

        Returns:
            List[PriceDataPoint]: List of today's price data points.
        """
        data = await self.price_data_latest()
        if data:
            now_fi = datetime.now(ZoneInfo("Europe/Helsinki"))
            today_fi = now_fi.date()
            filtered_data = [item for item in data if item.startDate.astimezone(ZoneInfo("Europe/Helsinki")).date() == today_fi]
            return sorted(filtered_data, key=lambda x: x.startDate, reverse=True)
        else:
            return await self.ext_api_fetcher.fetch_price_data_today()
    

