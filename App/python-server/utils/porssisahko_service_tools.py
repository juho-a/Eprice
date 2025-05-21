from models.data_model import *
from ext_apis.ext_apis import *
from repositories.porssisahko_repository import *
from utils.porssisahko_service_tools import *
from config.secrets import DATABASE_URL
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class PorssisahkoServiceTools:
    """
    Helper service for time range calculations, data conversion, and filling missing entries.
    """

    def __init__(self, ext_api_fetcher: FetchPriceData, database_fetcher: PorssisahkoRepository):
        """
        Initialize the HelperService with external API and database fetchers.
        """
        self.ext_api_fetcher = ext_api_fetcher
        self.database_fetcher = database_fetcher

    def expected_time_range(self) -> tuple[datetime, datetime]:
        """
        Calculate the expected time range for the latest 48 hours based on Helsinki time.

        Returns:
            tuple[datetime, datetime]: Start and end datetimes (naive).
        """
        now_naive = datetime.now(ZoneInfo("Europe/Helsinki")).replace(tzinfo=None)
        if now_naive.hour >= 14:
            end_time = (now_naive + timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            end_time = (now_naive + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = (end_time - timedelta(hours=48)).replace(tzinfo=None)
        return start_time, end_time

    def _convert_to_price_data(self, data: List[dict]) -> List[PriceDataPoint]:
        """
        Convert a list of database dicts to a sorted list of PriceDataPoint objects in UTC.

        Args:
            data (List[dict]): List of dicts with 'datetime' and 'price'.

        Returns:
            List[PriceDataPoint]: Sorted list of PriceDataPoint objects.
        """
        return sorted([
            PriceDataPoint(
                startDate=item["datetime"].astimezone(ZoneInfo("UTC")),
                price=item["price"]
            ) for item in data
        ], key=lambda x: x.startDate, reverse=True)

    async def _fill_missing_entries(self, result: List[PriceDataPoint], missing_entries: List[PriceDataPoint]):
        """
        Fetch and insert missing price data entries from the external API.

        Args:
            result (List[PriceDataPoint]): List to append new data points to.
            missing_entries (List[PriceDataPoint]): List of missing data points to fetch.
        """
        for missing in missing_entries:
            fetched = await self.ext_api_fetcher.fetch_price_data_range(missing.startDate, missing.startDate)
            if not fetched:
                continue

            datapoint = fetched[0]
            utc_dt = datetime.fromisoformat(datapoint["startDate"])
            iso_str = (utc_dt + timedelta(hours=3)).replace(microsecond=0).isoformat().replace("+00:00", "Z")

            result.append(PriceDataPoint(
                startDate=utc_dt,
                price=datapoint["price"]
            ))

            await self.database_fetcher.insert_entry(
                price=datapoint["price"],
                iso_date=iso_str
            )

    async def fetch_and_process_data(self, start_date: datetime, end_date: datetime) -> List[PriceDataPoint]:
        """
        Fetch and process price data from the database, fill missing entries from the external API if needed.

        Args:
            start_date (datetime): Start of the time range.
            end_date (datetime): End of the time range.

        Returns:
            List[PriceDataPoint]: Sorted list of price data points for the range.
        """
        start_naive = start_date.replace(tzinfo=None)
        end_naive = end_date.replace(tzinfo=None)

        raw_data = await self.database_fetcher.get_entries(
            start_date=start_naive,
            end_date=end_naive,
            select_columns="datetime, price"
        )
        if not raw_data:
            return []

        result = self._convert_to_price_data(raw_data)

        missing_entries = self.find_missing_entries_utc(
            start_date.astimezone(ZoneInfo("UTC")),
            end_date.astimezone(ZoneInfo("UTC")),
            result
        )
        if missing_entries:
            await self._fill_missing_entries(result, missing_entries)

        return sorted(result, key=lambda x: x.startDate, reverse=True)

    def find_missing_entries_utc(self, start_date_utc: datetime, end_date_utc: datetime, data_utc: List[PriceDataPoint]):
        """
        Find missing hourly entries in the given UTC time range.

        Args:
            start_date_utc (datetime): Start of the UTC time range.
            end_date_utc (datetime): End of the UTC time range.
            data_utc (List[PriceDataPoint]): List of available data points.

        Returns:
            List[StartDateModel]: List of StartDateModel objects for missing hours.
        """
        result = []
        current_date_utc = start_date_utc
        while current_date_utc <= end_date_utc:
            if not any(item.startDate == current_date_utc for item in data_utc):
                result.append(StartDateModel(startDate=current_date_utc))
            current_date_utc += timedelta(hours=1)
        result.sort(key=lambda x: x.startDate, reverse=True)
        return result
