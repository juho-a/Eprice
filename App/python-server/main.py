from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import router as auth_router
from controllers.auth_controller import create_jwt_middleware
import httpx

# Public routes that do not require authentication
# These routes can be accessed without a valid JWT token
public_routes = [
    "/api/public/data",
    "/api/auth/login",
    "/api/auth/register",
    "/api/prices",
]

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173", "http://localhost:5173"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# Include the auth routes
app.include_router(auth_router)
# Middleware to check JWT token
# everything that's not in public routes has to have a valid JWT token
app.middleware("http")(create_jwt_middleware(public_routes))


# example data endpoints
@app.get("/api/data")
async def get_data():
    '''Example data endpoint

    Returns:
        dict: A dictionary containing example data for the chart.
        dict has the following keys:
            - chartType: str, type of chart (e.g., 'bar', 'line', etc.), default is 'bar'
            - chartValues: list of int
            - chartLabels: list of str

        	chartValues = [20, 10, 5, 2, 20, 30, 45];
	        chartLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    '''
    chartType = 'bar'
    chartValues = [20, 10, 5, 2, 20, 30, 45]
    chartLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    return {
        'chartType': chartType,
        'chartValues': chartValues,
        'chartLabels': chartLabels
    }

@app.get("/api/public/data")
async def get_prices():
    """
    Fetch the latest prices from the external API and extract prices and hours.

    Returns:
        dict: A dictionary with keys 'values' (prices) and 'labels' (hours).
    """
    url = "https://api.porssisahko.net/v1/latest-prices.json"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()  # Parse the JSON response

            # Extract prices and hours
            prices = [item["price"] for item in data["prices"]]
            hours = [item["startDate"][11:16] for item in data["prices"]]  # Extract hour (HH:MM) from startDate
            assert len(prices) == len(hours), "Prices and hours lists must be of the same length"
            
            # sort the prices and hours by hour
            prices, hours = zip(*sorted(zip(prices, hours), key=lambda x: x[1]))
            
            # Convert prices to float
            prices = [float(price) for price in prices]
            # Convert hours to string
            hours = list(range(24))#[str(hour) for hour in hours]
            
            return {
                "chartLegend": "Prices (snt / kWh)",
                "chartType": "bar",
                "chartValues": prices,
                "chartLabels": hours,
                "message": "Prices fetched successfully"
            }
    except httpx.RequestError as exc:
        return {"error": f"An error occurred while requesting {exc.request.url}: {str(exc)}"}
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}"}

