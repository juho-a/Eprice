# List of all endpoints:
**Authentication**
- POST /api/auth/register
- POST /api/auth/login 
- GET /api/auth/logout

**Fingrid data**
- POST [api/public/windpower/range](#windpower-history-and-forecast)
- GET [api/public/windpower](#windpower-history-and-forecast)
- POST [/api/public/production/range](#total-production-history-and-forecast)
- GET [/api/public/production](#total-production-history-and-forecast)
- POST [/api/public/consumption/range](#consumption-forecast)
- GET [/api/public/consumption](#consumption-forecast)


**Weather forecast**
- POST api/public/weather/range
- GET api/public/weather



# Descriptions and examples of endpoints for Fingrid data
## Windpower history and forecast
Finnish wind power generation forecast and history data for the next 72 hours. Updated every 15 minutes. The forecast is based on weather forecasts and data about the location, size and capacity of wind turbines. The weather data sourced from multiple providers. The Data before 31.05.2023 is in hourly resolution.

## Total production history and forecast
The calculation of production forecast of all power prooduction types in Finland is based on the production plans that balance responsible parties has reported to Fingrid. Production forecast is updated every 15 minutes. The Data before 03.06.2023 is in hourly resolution."

## Consumption forecast
A consumption forecast for the next 24 hours made by Fingrid. Forecast is published on previous day at 12:00 EET. The Data before 21.04.2024 is in 5 minute resolution.

# Example requests and responses for fingrid data

Currently supported values for "data_name":
- windpower
- production
- consumption
```
POST http://localhost:8000/api/public/{data_name}/range
Content-Type: application/json
{
  "startTime": "2025-05-08T04:00:00Z",
  "endTime": "2025-05-08T06:00:00Z"
}
```
**Response:**
- `200 OK`: Windpower data in json format
- `???`: request failed

**Response of successful query in json format**
```
[
  {
    "startTime": "2025-05-08T04:00:00.000Z",
    "endTime": "2025-05-08T04:15:00.000Z",
    "value": 860.3
  },
  {
    "startTime": "2025-05-08T04:15:00.000Z",
    "endTime": "2025-05-08T04:30:00.000Z",
    "value": 831.7
  },
  {
    "startTime": "2025-05-08T04:30:00.000Z",
    "endTime": "2025-05-08T04:45:00.000Z",
    "value": 803.2
  }
]
```
### Current wind power production
```
GET http://localhost:8000/api/public/windpower
```

**Example response of failed request**
```
{"error": error details}
```