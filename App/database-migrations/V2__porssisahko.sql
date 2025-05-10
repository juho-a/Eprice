-- JUHO & MARKUS: 
-- Uncomment the line below if you want to drop the table first
-- There might be some issues with the unique constraint
-- But first try tearing down the containers and up again
--DROP TABLE IF EXISTS porssisahko;


DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'porssisahko') THEN
        CREATE TABLE porssisahko (
            id SERIAL PRIMARY KEY,
            Date DATE NOT NULL, -- New column for the date
            Year INT NOT NULL, -- Year for statistics
            Month INT NOT NULL,
            Day INT NOT NULL,
            Hour INT NOT NULL,
            Weekday INT NOT NULL,
            Price NUMERIC(10, 3) NOT NULL,
            Datetime TIMESTAMP NOT NULL -- New column for the datetime
        );

        -- Add a unique constraint to prevent duplicate rows
        ALTER TABLE porssisahko
            ADD CONSTRAINT unique_row UNIQUE (Datetime);
    END IF;
END $$;

-- Ensure the unique constraint exists
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.table_constraints
        WHERE table_name = 'porssisahko'
          AND constraint_name = 'unique_row'
    ) THEN
        ALTER TABLE porssisahko ADD CONSTRAINT unique_row UNIQUE (Datetime);
    END IF;
END $$;

-- Create a temporary table for staging the data
CREATE TEMP TABLE porssisahko_staging (
    Date DATE,
    Year INT,
    Month INT,
    Day INT,
    Hour INT,
    Weekday INT,
    Price NUMERIC(10, 3),
    Datetime TIMESTAMP
);

-- Load data into the temporary table
COPY porssisahko_staging (Date, Year, Month, Day, Hour, Weekday, Price, Datetime)
FROM '/data/porssisahko.csv'
WITH CSV HEADER DELIMITER ';';

-- Insert unique rows into the target table
INSERT INTO porssisahko (Date, Year, Month, Day, Hour, Weekday, Price, Datetime)
SELECT Date, Year, Month, Day, Hour, Weekday, Price, Datetime
FROM porssisahko_staging
ON CONFLICT (Datetime) DO NOTHING;

-- Drop the temporary table
DROP TABLE porssisahko_staging;