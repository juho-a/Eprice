-- JUHO & MARKUS: 
-- Uncomment the line below if you want to drop the table first
-- There might be some issues with the unique constraint
-- But first try tearing down the containers and up again
DROP TABLE IF EXISTS porssisahko;


DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'porssisahko') THEN
        CREATE TABLE porssisahko (
            id SERIAL PRIMARY KEY,
            Year INT NOT NULL, -- we use int so that we can get statistics
            Month INT NOT NULL,
            Day INT NOT NULL,
            Hour INT NOT NULL,
            Weekday INT NOT NULL,
            Price NUMERIC(10, 3) NOT NULL
        );

        -- Add a unique constraint to prevent duplicate rows
        ALTER TABLE porssisahko
            ADD CONSTRAINT unique_row UNIQUE (Year, Month, Day, Hour);
    END IF;
END $$;

-- JUHO & MARKUS: this is a bit stupid, but this is the only way I could
-- make sure there are no duplicates in the table

-- Create a temporary table for staging the data
CREATE TEMP TABLE porssisahko_staging (
    Year INT,
    Month INT,
    Day INT,
    Hour INT,
    Weekday INT,
    Price NUMERIC(10, 4)
);

-- Load data into the temporary table
COPY porssisahko_staging (Year, Month, Day, Hour, Weekday, Price)
FROM '/data/porssisahko.csv'
WITH CSV HEADER DELIMITER ';';

-- Insert unique rows into the target table
INSERT INTO porssisahko (Year, Month, Day, Hour, Weekday, Price)
SELECT Year, Month, Day, Hour, Weekday, Price
FROM porssisahko_staging
ON CONFLICT (Year, Month, Day, Hour) DO NOTHING;

-- Drop the temporary table
DROP TABLE porssisahko_staging;