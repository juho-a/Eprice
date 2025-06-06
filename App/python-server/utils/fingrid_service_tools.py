from models.data_model import *
from ext_apis.ext_apis import *
from repositories.fingrid_repository import *
from utils.porssisahko_service_tools import *
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class FingridServiceTools:
    """
    A class containing utility methods for Fingrid-related operations.
    """
    def __init__(self, ext_api_fetcher, fingrid_repository):
        """
        Initialize the FingridTools with the FingridRepository.
        This repository is used to interact with the Fingrid database.
        """
        self.fingrid_repository = fingrid_repository
        self.ext_api_fetcher = ext_api_fetcher

    async def fetch_and_process_data(self, time_range:TimeRange, dataset_id: int):
        """
        Fetch and process Fingrid data for a given dataset ID.
        
        Args:
            dataset_id (int): The Fingrid dataset ID.
        
        Returns:
            List[FingridDataPoint]: Processed list of Fingrid data points.
        """
        try:
            start_naive_hki = time_range.startTime.astimezone(ZoneInfo("Europe/Helsinki")).replace(tzinfo=None)
            end_naive_hki = time_range.endTime.astimezone(ZoneInfo("Europe/Helsinki")).replace(tzinfo=None)


            raw_data = await self.fingrid_repository.get_entries(
                start_date=start_naive_hki,
                end_date=end_naive_hki,
                dataset_id=dataset_id,
                select_columns="datetime, value, dataset_id"
            )

            result = self.convert_to_fingrid_data(raw_data)

            missing_entries = self.find_missing_entries_utc(time_range, result, dataset_id)
            if missing_entries:
                print(f"Database has {len(missing_entries)} entries missing in the range {time_range.startTime} to {time_range.endTime} with dataset ID {dataset_id}.")
                await self.fill_missing_entries(result, missing_entries, dataset_id)
            return sorted(result, key=lambda x: x.startTime, reverse=False)
        except Exception as e:
            print(f"Error while fetching and processing data: {e}")
            raise

        

    def convert_to_fingrid_data(self, data: List[dict]) -> List[FingridDataPoint]:
        """
        Convert a list of database dicts to a sorted list of PriceDataPoint objects in UTC.

        Args:
            data (List[dict]): List of dicts with 'datetime' and 'price'.

        Returns:
            List[PriceDataPoint]: Sorted list of PriceDataPoint objects (startDate in UTC).
        """
        if not data:
            return []
        return sorted([
            FingridDataPoint(
                startTime=item["datetime"].astimezone(ZoneInfo("UTC")),
                endTime=(item["datetime"] + timedelta(hours=1)).astimezone(ZoneInfo("UTC")),
                value=float(item["value"])
            ) for item in data
        ], key=lambda x: x.startTime, reverse=False)


    def find_missing_entries_utc(self, time_range:TimeRange, data_utc: List[FingridDataPoint], dataset_id: int) -> List[StartDateModel]:
        """
        Find missing hourly entries in the given UTC time range.

        Args:
            start_date_utc (datetime): Start of the UTC time range.
            end_date_utc (datetime): End of the UTC time range.
            data_utc (List[PriceDataPoint]): List of available data points.

        Returns:
            List[StartDateModel]: List of StartDateModel objects for missing hours (all in UTC).
        """
        result = []
        current_date_utc = time_range.startTime
        try:
            while current_date_utc <= time_range.endTime:
                if not any(item.startTime == current_date_utc for item in data_utc):
                    result.append(StartDateModel(startDate=current_date_utc))
                current_date_utc += timedelta(hours=1)
            result.sort(key=lambda x: x.startDate, reverse=False)
        except Exception as e:
            print(f"Error while finding missing entries: {e}")
            raise
        return result
    
    async def fill_missing_entries(self, result: List[FingridDataPoint], missing_entries: List[StartDateModel], dataset_id: int):
        """
        Fetch and insert missing price data entries from the external API.

        Args:
            result (List[PriceDataPoint]): List to append new data points to (modified in place).
            missing_entries (List[PriceDataPoint]): List of missing data points to fetch.

        Side effects:
            Updates the result list and inserts new entries into the database.
        """

        self.result = result
        if not missing_entries:
            return
        start_time_utc_aware = min(missing_entries, key=lambda x: x.startDate).startDate
        end_time_utc_aware = max(missing_entries, key=lambda x: x.startDate).startDate
        time_range = TimeRange(startTime=start_time_utc_aware, endTime=end_time_utc_aware + timedelta(hours=1))
        
        try:
            # Fetch data for entire range of missing entries
            fetched_range = await self.ext_api_fetcher.fetch_fingrid_data_range(dataset_id, time_range)
            if not fetched_range:
                print("No data fetched for the missing entries range.")
                return
            print(f"Fetched {len(fetched_range)} entries for the range {time_range.startTime} to {time_range.endTime} from external API for dataset ID {dataset_id}.")
            counter = 0
            for entry in fetched_range:
                #if entry not in result:
                if any(item.startTime == entry.startTime for item in result):
                    continue
                utc_dt = entry.startTime
                iso_str = (utc_dt + timedelta(hours=0)).replace(microsecond=0).isoformat().replace("+00:00", "Z")

                result.append(FingridDataPoint(
                    startTime=utc_dt,
                    endTime=utc_dt + timedelta(hours=1),
                    value=entry.value
                ))
                await self.fingrid_repository.insert_entry(
                    value=entry.value,
                    iso_date=iso_str,
                    dataset_id=dataset_id
                )
                counter += 1
            print(f"Inserted {counter} missing entries into the database for dataset ID {dataset_id}.")
            # for missing in missing_entries:
            #     time_range = TimeRange(startTime=missing.startDate, endTime=missing.startDate + timedelta(hours=1))
            #     fetched = await self.ext_api_fetcher.fetch_fingrid_data_range(dataset_id, time_range)
            #     if not fetched:
            #         continue

            #     datapoint = fetched[0]

            #     utc_dt = datapoint.startTime
            #     iso_str = (utc_dt + timedelta(hours=0)).replace(microsecond=0).isoformat().replace("+00:00", "Z")

            #     result.append(FingridDataPoint(
            #         startTime=utc_dt,
            #         endTime=utc_dt + timedelta(hours=1),
            #         value=datapoint.value
            #     ))
            #     await self.fingrid_repository.insert_entry(
            #         value=datapoint.value,
            #         iso_date=iso_str,
            #         dataset_id=dataset_id
            #     )
        except Exception as e:
            print(f"Error while filling missing entries: {e}")

def convert_to_fingrid_entry(value, iso_date, predicted=False, convert_to_helsinki_time=True, dataset_id=-1):
    """
    Converts a price and ISO 8601 date into a dictionary for the porssisahko table.

    Args:
        price (float): The price value.
        iso_date (str): The date in ISO 8601 format (e.g., "2022-11-14T22:00:00.000Z").
        predicted (bool): Indicates if the price is predicted. Default is False.
    Returns:
        dict: A dictionary with keys: Datetime, Date, Year, Month, Day, Hour, Weekday, Price, Predicted.
    Raises:
        ValueError: If the ISO date is not in the correct format.
    """
  
    try:
        if convert_to_helsinki_time:
            # Parse the ISO date string to a UTC datetime
            dt_utc = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
            # Convert to Helsinki time
            dt_helsinki = dt_utc.astimezone(ZoneInfo("Europe/Helsinki"))
            dt_naive = dt_helsinki.replace(tzinfo=None)
        else:
            # Parse the ISO date string to a naive datetime (UTC)
            dt_naive = datetime.fromisoformat(iso_date.replace("Z", "+00:00")).replace(tzinfo=None)
        # Extract the weekday
        weekday = dt_naive.weekday()

        # Return the dictionary
        return {
            "datetime_orig": iso_date,  # Original datetime in UTC
            "datetime": dt_naive,  # Use offset-naive datetime
            "date": dt_naive.date(),  # Extract the date part
            "year": dt_naive.year,
            "month": dt_naive.month,
            "day": dt_naive.day,
            "hour": dt_naive.hour,
            "weekday": weekday,
            "dataset_id": dataset_id,
            "value": value,
            "predicted": predicted
        }
    except ValueError as e:
        # Handle invalid date format or parsing errors
        raise ValueError(f"Invalid ISO date format: {iso_date}. Error: {e}")


