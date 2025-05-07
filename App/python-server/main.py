from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import router as auth_router
from controllers.auth_controller import create_jwt_middleware
from external_apis.ext_apis import router as external_api_router


# Public routes that do not require authentication
# These routes can be accessed without a valid JWT token
public_routes = [
    "/api/public/data",
    "/api/auth/login",
    "/api/auth/register",
    "/api/latest_prices",
    "/api/public/weather",
    "/api/public/windpower",
    "/api/public/windpower/range",
    "/api/public/consumption",
    "/api/public/consumption/range"
    "/api/public/production",
    "/api/public/production/range"
    ]

app = FastAPI()
app.include_router(external_api_router)

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
