DROP TABLE IF EXISTS porssisahko;

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
    ADD CONSTRAINT porssisahko_datetime_key UNIQUE (Datetime);
