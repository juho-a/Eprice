-- Create a temporary table for staging the data
CREATE TEMP TABLE porssisahko_staging (
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

-- Load data into the temporary table
COPY porssisahko_staging (Datetime, Date, Year, Month, Day, Hour, Weekday, Price)
FROM '/data/porssisahko.csv'
WITH CSV HEADER DELIMITER ';';

-- Insert unique rows into the target table
INSERT INTO porssisahko (Datetime, Date, Year, Month, Day, Hour, Weekday, Price)
SELECT Datetime, Date, Year, Month, Day, Hour, Weekday, Price
FROM porssisahko_staging
ON CONFLICT (Datetime) DO NOTHING;

-- Drop the temporary table
DROP TABLE porssisahko_staging;
