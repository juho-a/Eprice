import os

# Database configuration
# check if environment variables for postgres are set, otherwise use default values
# Default values are for development purposes only
# and should not be used in production

if os.getenv("POSTGRES_USER") is None:
    os.environ["POSTGRES_USER"] = "username"
if os.getenv("POSTGRES_PASSWORD") is None:
    os.environ["POSTGRES_PASSWORD"] = "password"
if os.getenv("PGHOST") is None:
    os.environ["PGHOST"] = "postgresql_database"
if os.getenv("PGPORT") is None:
    os.environ["PGPORT"] = "5432"
if os.getenv("POSTGRES_DB") is None:
    os.environ["POSTGRES_DB"] = "database"

# PostgreSQL connection string
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('POSTGRES_DB')}"
# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "wsd-project-secret")  # Default value for development
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default algorithm
COOKIE_KEY = os.getenv("COOKIE_KEY", "token")  # Default cookie key
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Public routes that do not require authentication
# These routes can be accessed without a valid JWT token
public_routes = [
    "/email",
    "/api/public/data",
    "/api/public/data/today",
    "/api/auth/login",
    "/api/auth/register",
    "/api/auth/verify",
    "/api/auth/resend",
    "/api/latest_prices",
    "/api/public/weather",
    "/api/public/weather/range",
    "/api/public/windpower",
    "/api/public/windpower/range",
    "/api/public/consumption",
    "/api/public/consumption/range",
    "/api/public/production",
    "/api/public/production/range",
    "/api/public/price/range",
    "/docs",
    "/openapi.json"
    ]