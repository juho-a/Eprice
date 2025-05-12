import asyncpg
from utils.porssisahko_tools import convert_to_porssisahko_entry

class PorssisahkoRepository:
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def insert_entry(self, price: float, iso_date: str, predicted: bool = False):
        """
        Inserts a single entry into the porssisahko table.

        Args:
            price (float): The price value.
            iso_date (str): The date in ISO 8601 format.
            predicted (bool): Indicates if the price is predicted. Default is False.
        Returns:
            None
        """
        conn = None
        try:
            # Convert the entry to the correct format
            entry = convert_to_porssisahko_entry(price, iso_date, predicted)

            # Connect to the database
            conn = await asyncpg.connect(self.database_url)

            # Insert the entry into the database
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
            print(f"Database error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        finally:
            if conn:
                await conn.close()

    async def insert_entries(self, entries: list):
        """
        Inserts multiple entries into the porssisahko table.

        Args:
            entries (list[dict]): A list of dictionaries containing the data to insert.
        Returns:
            None
        """
        conn = None
        try:
            # Convert entries to the correct format
            formatted_entries = [
                convert_to_porssisahko_entry(entry["price"], entry["startDate"], predicted=entry.get("predicted", False))
                for entry in entries
            ]

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
                for entry in formatted_entries
            ]

            # Connect to the database
            conn = await asyncpg.connect(self.database_url)

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

    async def get_entries(self, start_date: str, end_date: str, select_columns: str = "*"):
        """
        Retrieves entries from the porssisahko table between two dates.

        Args:
            start_date (str): The start date in ISO 8601 format.
            end_date (str): The end date in ISO 8601 format.
            select_columns (str): The columns to select from the table. Default is "*".
        Returns:
            list[dict]: A list of dictionaries containing the data for each entry.
        """
        conn = None
        try:
            # Connect to the database
            conn = await asyncpg.connect(self.database_url)

            # Execute the query
            rows = await conn.fetch(
                f"""
                SELECT {select_columns}
                FROM porssisahko
                WHERE Datetime BETWEEN $1 AND $2
                """,
                start_date,
                end_date
            )

            # Convert rows to a list of dictionaries
            return [dict(row) for row in rows]
        except asyncpg.PostgresError as e:
            print(f"Database error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        finally:
            if conn:
                await conn.close()

    async def get_missing_entries(self, start_date: str, end_date: str):
        """
        Retrieves missing entries from the porssisahko table between two dates.

        Args:
            start_date (str): The start date in ISO 8601 format.
            end_date (str): The end date in ISO 8601 format.
        Returns:
            list[tuple]: A list of tuples where each tuple contains the date (YYYY-MM-DD) and hour (0-23).
        """
        conn = None
        try:
            # Connect to the database
            conn = await asyncpg.connect(self.database_url)

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

            # Return the missing entries as a list of tuples
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