-- Drop the existing porssisahko table (if necessary)
DROP TABLE IF EXISTS porssisahko;

-- Create the updated porssisahko table
CREATE TABLE porssisahko (
    id SERIAL PRIMARY KEY,
    Year INT NOT NULL,
    Month INT NOT NULL,
    Day INT NOT NULL,
    Hour INT NOT NULL,
    Weekday INT NOT NULL,
    Price NUMERIC(10, 2) NOT NULL
);

-- Populate the porssisahko table from the CSV file
COPY porssisahko (Year, Month, Day, Hour, Weekday, Price)
FROM '/data/porssisahko.csv'
WITH CSV HEADER DELIMITER ';';