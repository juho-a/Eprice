from pydantic import BaseModel, Field
from pydantic import BaseModel, field_validator
from datetime import datetime


class DateTimeValidatedModel(BaseModel):
    @classmethod
    @field_validator('startTime', 'endTime', 'timestamp', 'startDate', mode='before')
    def validate_datetime(cls, v):
        datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v

class StartDateModel(BaseModel):
    startDate: datetime

class TimeRange(DateTimeValidatedModel):
    startTime: datetime = Field(
        description="Start time in RFC 3339 format (e.g., 2024-05-01T00:00:00Z)",
        examples=["2024-05-01T00:00:00Z"]
    )
    endTime: datetime = Field(
        examples=["2024-05-02T00:00:00Z"],
        description="End time in RFC 3339 format (e.g., 2024-05-02T00:00:00Z)"
    )

class TimeRangeRequest(TimeRange):
    def start_datetime(self) -> datetime:
        # katso kommentti alla
        if isinstance(self.startTime, str):
            return datetime.fromisoformat(str(self.startTime).replace("Z", "+00:00"))
        elif isinstance(self.startTime, datetime):
            return self.startTime
        else:
            raise TypeError("startTime must be a string or datetime object")

    def end_datetime(self) -> datetime:
        # näille pitää ehkä tehdä vielä jotain tyyliin:
        # dt = datetime.fromisoformat(self.startTime.replace("Z", "+00:00"))
        # dt_naive = dt.replace(tzinfo=None) <-- tämä palautetaan
        # koska me ei laiteta tietokantaan sit' timezone tietoa ollenkaan
        if isinstance(self.endTime, str):
            return datetime.fromisoformat(str(self.endTime).replace("Z", "+00:00"))
        elif isinstance(self.endTime, datetime):
            return self.endTime
        else:
            raise TypeError("endTime must be a string or datetime object")


class FingridDataPoint(TimeRange):
    value: float = Field(
        examples=[7883.61],
        description="Value of the data point"
    )

    @field_validator("value")
    def validate_value_positive(cls, v):
        if v < 0:
            raise ValueError("value must be non-negative")
        return v

class PriceDataPoint(StartDateModel):
    startDate: datetime = Field(
        description="UTC str in RFC 3339 format",
        examples=["2025-05-08T04:00:00.000Z"]
    )
    price: float = Field(
        description="Floating-point number representing the price in euro cents",
        examples=[0.61]
    )

# Define a model for error responses
class ErrorResponse(BaseModel):
    error: str = Field(
        description="Error message describing the issue.",
        examples=["An error occurred"]
    )

