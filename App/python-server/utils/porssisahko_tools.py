from datetime import datetime, timedelta
import asyncpg
from config.secrets import DATABASE_URL

async def insert_into_porssisahko_table(entries: list, predicted: bool = False):
    """
    Inserts multiple entries into the porssisahko table.
    
    Args:
        entries (list[dict]): A list of dictionaries containing the data to insert.
        Each dictionary should have 'price' and 'startDate' keys. 
        They might also have 'endDate' key, but it is not used in this function.
        predicted (bool): Indicates if the entries are predicted. Default is False.
        NOTE: the predicted flag is for future use, and is not used in the current implementation.
    Returns:
        None    
    Raises:
        asyncpg.PostgresError: If there is an error with the database operation.
        Exception: If there is an unexpected error.
    """
    # Convert each entry to the appropriate format
    formatted_entries = [
        convert_to_porssisahko_entry(entry["price"], entry["startDate"], predicted=predicted)
        for entry in entries
    ]

    # Insert the entries into the database
    await insert_porssisahko_entries(formatted_entries)

async def get_missing_porssisahko_entries(start_date: str, end_date: str):
    """
    Retrieves missing entries from the porssisahko table between two dates.
    Args:
        start_date (str): The start date in ISO 8601 format (e.g., "2022-11-14T22:00:00.000Z").
        end_date (str): The end date in ISO 8601 format (e.g., "2022-11-14T22:00:00.000Z").
    Returns:
        list[tuple]: A list of tuples where each tuple contains the date (YYYY-MM-DD) and hour (0-23).
    Raises:
        asyncpg.PostgresError: If there is an error with the database operation.
        Exception: If there is an unexpected error.
    """
    conn = None
    try:
        conn = await asyncpg.connect(DATABASE_URL)

        # Execute the query to find missing entries
        rows = await conn.fetch(
            """
            WITH date_range AS (
                SELECT generate_series(
                    $1::TIMESTAMP,
                    $2::TIMESTAMP,
                    '1 hour'::INTERVAL
                ) AS Datetime
            )
            SELECT dr.Datetime
            FROM date_range dr
            LEFT JOIN porssisahko p ON dr.Datetime = p.Datetime
            WHERE p.Datetime IS NULL
            """,
            start_date,
            end_date
        )

        return [
            (row["Datetime"].strftime("%Y-%m-%d"), row["Datetime"].hour)
            for row in rows
        ]
    except asyncpg.PostgresError as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
    finally:
        if conn:
            await conn.close()

async def get_porssisahko_entries(start_date: str, end_date: str, select_columns: str = "*"):
    """
    Retrieves entries from the porssisahko table between two dates.

    Args:
        start_date (str): The start date in ISO 8601 format (e.g., "2022-11-14T22:00:00.000Z").
        end_date (str): The end date in ISO 8601 format (e.g., "2022-11-14T22:00:00.000Z").
        select_columns (str): The columns to select from the table. Default is "*".
    Returns:
        list[dict]: A list of dictionaries containing the data for each entry.
    Raises:
        asyncpg.PostgresError: If there is an error with the database operation.
        Exception: If there is an unexpected error.
    """
    conn = None
    try:
        conn = await asyncpg.connect(DATABASE_URL)

        # Execute the query to find missing entries
        rows = await conn.fetch(
            """
            SELECT {select_columns}
            FROM porssisahko
            WHERE Datetime BETWEEN $1 AND $2
            """.format(select_columns=select_columns),
            start_date,
            end_date
        )

        return [
            dict(row)
            for row in rows
        ]
    except asyncpg.PostgresError as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
    finally:
        if conn:
            await conn.close()


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


async def insert_porssisahko_entry(entry: dict):
    """
    Inserts a single entry into the porssisahko table using asyncpg.

    Args:
        database_url (str): The database connection URL.
        entry (dict): A dictionary containing the data to insert.
    Returns:
        None
    Raises:
        asyncpg.PostgresError: If there is an error with the database operation.
        Exception: If there is an unexpected error.
    """
    conn = None
    try:
        # Attempt to connect to the database
        conn = await asyncpg.connect(DATABASE_URL)

        # Execute the insert query
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
    except asyncpg.PostgresError as e:
        # Handle database-related errors
        print(f"Database error: {e}")
        raise # NOTE: Juho, this will propagate the error to the caller
    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        raise # NOTE: we get more granular error information this way
    finally:
        if conn: # has to be checked here --  trying to close a None connection will raise an error
            await conn.close()

async def insert_porssisahko_entries(entries: list):
    """
    Inserts multiple entries into the porssisahko table.

    Args:
        entries (list[dict]): A list of dictionaries containing the data to insert.
    Returns:
        None
    Raises:
        asyncpg.PostgresError: If there is an error with the database operation.
        Exception: If there is an unexpected error.
    """
    conn = None
    try:
        # Attempt to connect to the database
        conn = await asyncpg.connect(DATABASE_URL)

        # Prepare the insert query
        insert_query = """
            INSERT INTO porssisahko (Datetime, Date, Year, Month, Day, Hour, Weekday, Price)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (Datetime) DO NOTHING
        """
        # Create a list of tuples for the entries
        values = [
            (
                entry["Datetime"],
                entry["Date"],
                entry["Year"],
                entry["Month"],
                entry["Day"],
                entry["Hour"],
                entry["Weekday"],
                entry["Price"]
            )
            for entry in entries
        ]
        
        # Execute the insert query with the list of values
        await conn.executemany(insert_query, values)
    except asyncpg.PostgresError as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
    finally:
        if conn:
            await conn.close()
            
