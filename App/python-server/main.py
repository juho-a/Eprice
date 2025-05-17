from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import router as auth_router
from controllers.auth_controller import create_jwt_middleware
from controllers.data_controller import router as external_api_router

from utils.scheduled_tasks import shutdown_scheduler  # Import the shutdown function to clean up the scheduler
from utils.scheduled_tasks import fetch_and_insert_missing_porssisahko_data

from config.secrets import public_routes

from chat.engine import chat_app
from utils.email_tools import send_email_async

app = FastAPI()
app.include_router(external_api_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173",
                    "http://localhost:5173",
                    "http://testserver"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# Include the auth routes
app.include_router(auth_router)
# Middleware to check JWT token
# everything that's not in public routes has to have a valid JWT token
app.middleware("http")(create_jwt_middleware(public_routes))

# Include the chat route
app.mount("/chat", chat_app)

@app.on_event("startup")
async def startup_event():
    '''Startup event handler
    This function is called when the application starts.
    It checks for missing Pörssisähkö data and fetches it from the API.
    '''
    print("Server is starting... Checking for missing data.")
    start_datetime = "2025-05-13T23:00:00"  # NOTE: this is the last date in historical data
    await fetch_and_insert_missing_porssisahko_data(start_datetime)
    print("Server started and missing data checked.")

# To shut down the scheduler when the application is shutting down
@app.on_event("shutdown")
async def shutdown_event():
    '''Shutdown event handler
    This function is called when the application is shutting down.
    It cleans up the scheduler to prevent any background tasks from running after the application has stopped.
    '''
    shutdown_scheduler()

@app.get("/email")
async def send_email(
    email_to: str,
    verification_code: str
):
    '''Send an email to the user with the verification code'''
    await send_email_async(email_to, verification_code)
    return {"message": "Email sent"}
