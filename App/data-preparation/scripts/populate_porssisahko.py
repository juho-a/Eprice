# this script populates the porssisahko table in the database
# NOTE: environment variables are loaded by docker compose

# whatever dependencies you need, add them
# to Dockerfile or create a requirements.txt file
import psycopg2 # pip install psycopg2-binary
import pandas as pd
import sys


def populate_db(df):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect() # env is already loaded by docker compose
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS porssisahko (
            id SERIAL PRIMARY KEY,
            Date DATE,
            Year INT,
            Month INT,
            Day INT,
            Hour INT,
            Weekday INT,
            Price FLOAT
        )
    """)
    
    # add a unique constraint to the datetime column if it doesn't exist
    cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.table_constraints
                WHERE table_name = 'porssisahko'
                AND constraint_name = 'unique_date_time'
            ) THEN
                ALTER TABLE porssisahko ADD CONSTRAINT unique_date_time UNIQUE (Date, Hour);
            END IF;
        END $$;
    """)
    # Insert data into the table (on conflict do nothing)
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO porssisahko (Date, Year, Month, Day, Hour, Weekday, Price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (Date, Hour) DO NOTHING
        """, (row["Date"], row["Year"], row["Month"], row["Day"], row["Hour"], row["Weekday"], row["Price"]))
    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Data populated successfully.")
    print(f"Inserted {len(df)} rows into the database.")

if __name__ == "__main__":
    # Define the filename
    #filename = "../data/porssisahko.csv"
    filename = sys.argv[1]
    # Read the csv
    df = pd.read_csv(filename, sep=";", encoding="utf-8")
    # Populate the database
    populate_db(df)
    