"""
data_model.py

This module defines Pydantic data models used throughout the Eprice backend service.
It includes models for time ranges, Fingrid and price data points, error responses,
and utility base classes for datetime validation.
"""

from pydantic import BaseModel, Field
from pydantic import BaseModel, field_validator
from datetime import datetime

class DateTimeValidatedModel(BaseModel):
    """
    Base model that validates datetime fields to ensure they are in ISO 8601 format.
    Fields validated: 'startTime', 'endTime', 'timestamp', 'startDate'.
    """
    @classmethod
    @field_validator('startTime', 'endTime', 'timestamp', 'startDate', mode='before')
    def validate_datetime(cls, v):
        """
        Validates that the provided value is a valid ISO 8601 datetime string.
        """
        datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v

class StartDateModel(BaseModel):
    """
    Model containing a single startDate field as a datetime object.
    """
    startDate: datetime

class TimeRange(DateTimeValidatedModel):
    """
    Model representing a time range with start and end times.

    Attributes:
        startTime (datetime): Start time in RFC 3339 format.
        endTime (datetime): End time in RFC 3339 format.
    """
    startTime: datetime = Field(
        description="Start time in RFC 3339 format (e.g., 2024-05-01T00:00:00Z)",
        examples=["2024-05-01T00:00:00Z"]
    )
    endTime: datetime = Field(
        examples=["2024-05-02T00:00:00Z"],
        description="End time in RFC 3339 format (e.g., 2024-05-02T00:00:00Z)"
    )

class TimeRangeRequest(TimeRange):
    """
    Request model for endpoints requiring a time range.
    Provides helper methods to ensure start and end times are returned as datetime objects.
    """
    def start_datetime(self) -> datetime:
        """
        Returns the start time as a datetime object, parsing from string if necessary.

        Returns:
            datetime: The start time as a datetime object.
        """
        if isinstance(self.startTime, str):
            return datetime.fromisoformat(str(self.startTime).replace("Z", "+00:00"))
        elif isinstance(self.startTime, datetime):
            return self.startTime
        else:
            raise TypeError("startTime must be a string or datetime object")

    def end_datetime(self) -> datetime:
        """
        Returns the end time as a datetime object, parsing from string if necessary.

        Returns:
            datetime: The end time as a datetime object.
        """
        if isinstance(self.endTime, str):
            return datetime.fromisoformat(str(self.endTime).replace("Z", "+00:00"))
        elif isinstance(self.endTime, datetime):
            return self.endTime
        else:
            raise TypeError("endTime must be a string or datetime object")

class FingridDataPoint(TimeRange):
    """
    Model representing a single data point from Fingrid, including a value and time range.

    Attributes:
        value (float): Value of the data point, must be non-negative.
    """
    value: float = Field(
        examples=[7883.61],
        description="Value of the data point"
    )

    @field_validator("value")
    def validate_value_positive(cls, v):
        """
        Validates that the value is non-negative.

        Raises:
            ValueError: If the value is negative.
        """
        if v < 0:
            raise ValueError("value must be non-negative")
        return v

class PriceDataPoint(StartDateModel):
    """
    Model representing a single electricity price data point.

    Attributes:
        startDate (datetime): Start time of the price data point in UTC.
        price (float): Price in euro cents.
    """
    startDate: datetime = Field(
        description="UTC str in RFC 3339 format",
        examples=["2025-05-08T04:00:00.000Z"]
    )
    price: float = Field(
        description="Floating-point number representing the price in euro cents",
        examples=[0.61]
    )

class ErrorResponse(BaseModel):
    """
    Model for error responses returned by the API.

    Attributes:
        error (str): Error message describing the issue.
    """
    error: str = Field(
        description="Error message describing the issue.",
        examples=["An error occurred"]
    )

