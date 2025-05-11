DROP TABLE IF EXISTS porssisahko;

CREATE TABLE porssisahko (
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

-- Add a unique constraint to prevent duplicate rows (date and time)
ALTER TABLE porssisahko
    ADD CONSTRAINT unique_datetime UNIQUE (Datetime);
