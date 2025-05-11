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
            Datetime TIMESTAMP NOT NULL, -- Original column for datetime
            Date DATE NOT NULL, -- New column for the date
            Year INT NOT NULL, -- Year, etc. for statistics
            Month INT NOT NULL,
            Day INT NOT NULL,
            Hour INT NOT NULL,
            Weekday INT NOT NULL,
            Price NUMERIC(10, 3) NOT NULL,
            Predicted BOOLEAN NOT NULL DEFAULT FALSE,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # add a unique constraint to the datetime column if it doesn't exist
    cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.table_constraints
                WHERE table_name = 'porssisahko'
                AND constraint_name = 'unique_datetime'
            ) THEN
                ALTER TABLE porssisahko ADD CONSTRAINT unique_datetime UNIQUE (Datetime);
            END IF;
        END $$;
    """)
    # Insert data into the table (on conflict do nothing)
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO porssisahko (Datetime, Date, Year, Month, Day, Hour, Weekday, Price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (Datetime) DO NOTHING
        """, (row["Datetime"], row["Date"], row["Year"], row["Month"], row["Day"], row["Hour"], row["Weekday"], row["Price"]))
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
    