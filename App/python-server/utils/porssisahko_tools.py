from datetime import datetime
import asyncpg

def convert_to_porssisahko_entry(price, iso_date, predicted=False):
    """
    Converts a price and ISO 8601 date into a dictionary for the porssisahko table.

    Args:
        price (float): The price value.
        iso_date (str): The date in ISO 8601 format (e.g., "2022-11-14T22:00:00.000Z").
        predicted (bool): Indicates if the price is predicted. Default is False.
        If True, the price is considered a prediction.
        If False, the price is considered an actual value (historical).

    Returns:
        dict: A dictionary with keys: Datetime, Date, Year, Month, Day, Hour, Weekday, Price, Predicted.
    """
    # Parse the ISO 8601 date
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))  # Handle the "Z" for UTC

    # Extract components
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    weekday = dt.weekday()  # Monday = 0, Sunday = 6

    # Format Datetime and Date fields
    datetime_str = dt.strftime(f"%Y-%m-%d {hour:02d}:00:00")  # "YYYY-MM-DD HH:00:00"
    date_str = dt.strftime("%Y-%m-%d")  # "YYYY-MM-DD"

    # Return the dictionary
    return {
        "Datetime": datetime_str,
        "Date": date_str,
        "Year": year,
        "Month": month,
        "Day": day,
        "Hour": hour,
        "Weekday": weekday,
        "Price": price,
        "Predicted": predicted
    }

async def insert_porssisahko_entry(database_url: str, entry: dict):
    """
    Inserts a single entry into the porssisahko table using asyncpg.

    Args:
        database_url (str): The database connection URL.
        entry (dict): A dictionary containing the data to insert.
    """
    # assumes correct database_url format
    conn = await asyncpg.connect(database_url)
    try:
        await conn.execute(
            """
            INSERT INTO porssisahko (Datetime, Date, Year, Month, Day, Hour, Weekday, Price)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (Datetime) DO NOTHING
            """,
            entry["Datetime"],
            entry["Date"],
            entry["Year"],
            entry["Month"],
            entry["Day"],
            entry["Hour"],
            entry["Weekday"],
            entry["Price"]
        )
    finally:
        await conn.close()