from pydantic import BaseModel, Field

class TimeRangeRequest(BaseModel):
    startTime: str = Field(
        example="2024-05-01T00:00:00Z",
        description="Start time in RFC 3339 format (e.g., 2024-05-01T00:00:00Z)"
    )
    endTime: str = Field(
        example="2024-05-02T00:00:00Z",
        description="End time in RFC 3339 format (e.g., 2024-05-02T00:00:00Z)"
    )

class WeatherRequest(BaseModel):
    lat: float = Field(..., description="Latitude", example=60.1699)
    lon: float = Field(..., description="Longitude", example=24.9384)
    timestamp: str = Field(..., description="UTC datetime in RFC 3339 format, e.g. 2024-05-05T13:30:00Z", example="2024-05-05T13:30:00Z")

class WeatherDataPoint(BaseModel):
    temperature_celsius: float = Field(..., example=8.5)
    wind_speed_mps: float = Field(..., example=2.2)
    closest_forecast_time: str = Field(..., example="2025-05-09T16:00:00Z")

class PriceData(BaseModel):
    time: str = Field(..., example="2025-05-08T04:00:00.000Z")
    price: float = Field(..., example=10.01)

class DataPoint(BaseModel):
    startTime: str = Field(..., example="2025-05-08T04:00:00.000Z")
    endTime: str = Field(..., example="2025-05-08T04:15:00.000Z")
    value: float = Field(..., example=7883.61)

# Define a model for Fingrid data
class FingridData(BaseModel):
    startTime: str= Field(
        example="2024-05-01T00:00:00Z",
        description="Start time in RFC 3339 format (e.g., 2024-05-01T00:00:00Z)"
    )
    endTime: str = Field(
        example="2024-05-02T00:00:00Z",
        description="End time in RFC 3339 format (e.g., 2024-05-02T00:00:00Z)"
    )
    value: float  = Field(
        example="7883.61",
        description="Value of the data point"
    )

class PriceDataPoint(BaseModel):
    startDate: str = Field(..., description="UTC datetime in RFC 3339 format", example="2025-05-08T04:00:00.000Z")
    price: float = Field(..., description="Floating-point number representing the price in euro cents", example=0.61)

# Define a model for error responses
class ErrorResponse(BaseModel):
    error: str

