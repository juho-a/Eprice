from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import router as auth_router
from controllers.auth_controller import create_jwt_middleware
from controllers.data_controller import router as external_api_router

from scheduled_tasks.porssisahko_scheduler import shutdown_scheduler, fetch_and_insert_missing_porssisahko_data

import config
from config.secrets import public_routes

from models.custom_exception import custom_validation_exception_handler
from fastapi.exceptions import RequestValidationError

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Server is starting... Checking for missing data.")
    start_datetime = "2025-05-13T23:00:00"
    await fetch_and_insert_missing_porssisahko_data(start_datetime)
    print("Server started and missing data checked.")
    yield
    # Shutdown code
    shutdown_scheduler()

app = FastAPI(lifespan=lifespan)
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.include_router(external_api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173",
                   "http://localhost:5173",
                   "http://testserver",
                   "http://192.168.10.46:5173",
                   "http://80.221.17.169:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.middleware("http")(create_jwt_middleware(public_routes))
