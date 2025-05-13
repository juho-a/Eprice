from datetime import datetime
import asyncpg
import time

async def wait_for_database(database_url):
    max_retries = 10
    retry_delay = 5  # seconds
    for attempt in range(max_retries):
        try:
            conn = await asyncpg.connect(database_url)
            await conn.close()
            print("Database is ready.")
            return
        except Exception as e:
            print(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    raise Exception("Database is not ready after multiple attempts.")


def convert_to_porssisahko_entry(price, iso_date, predicted=False):
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
        # Juho: we'll later make the formats more precise and succinct
        # Now there's some needless formatting to make the api play nice with the database
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))  # Handle the "Z" for UTC

        # Convert to offset-naive datetime (db doesn't like tz's)
        dt_naive = dt.replace(tzinfo=None)

        # Extract the weekday
        weekday = dt_naive.weekday()

        # Return the dictionary
        return {
            "Datetime": dt_naive,  # Use offset-naive datetime
            "Date": dt_naive.date(),  # Extract the date part
            "Year": dt_naive.year,
            "Month": dt_naive.month,
            "Day": dt_naive.day,
            "Hour": dt_naive.hour,
            "Weekday": weekday,
            "Price": price,
            "Predicted": predicted
        }
    except ValueError as e:
        # Handle invalid date format or parsing errors
        raise ValueError(f"Invalid ISO date format: {iso_date}. Error: {e}")


