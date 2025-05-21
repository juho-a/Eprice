import asyncio
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
#from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from repositories.porssisahko_repository import PorssisahkoRepository
from config.secrets import DATABASE_URL

# Initialize the repository with the database URL
porssisahko_repository = PorssisahkoRepository(DATABASE_URL)

# The task to fetch data and insert it into the database
async def fetch_and_insert_porssisahko_data():
    try:
        # Fetch data from the API
        response = requests.get("https://api.porssisahko.net/v1/latest-prices.json")
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()

        # Insert the data into the database using the repository
        await porssisahko_repository.insert_entries(data["prices"])

        print(f"Database successfully updated at {datetime.now()}")
    except requests.RequestException as e:
        print(f"Error fetching data from the API: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


async def fetch_and_insert_missing_porssisahko_data(start_datetime_str: str):
    try:
        # Convert the start_datetime string to a datetime object (db likes ISO format)
        start_datetime = datetime.fromisoformat(start_datetime_str)
        
        # Get the current datetime
        end_datetime = datetime.utcnow()
        end_datetime = end_datetime.replace(minute=0, second=0, microsecond=0)
        
        # Retrieve missing entries from the repository
        missing_entries = await porssisahko_repository.get_missing_entries(
            start_datetime, end_datetime
        )

        if not missing_entries:
            print(f"No missing entries found between {start_datetime} and {end_datetime}.")
            return

        print(f"Found {len(missing_entries)} missing entries. Fetching data...")

        # Fetch data for the missing entries
        for date, hour in missing_entries:
            # Construct the API URL for the specific date and hour
            api_url = f"https://api.porssisahko.net/v1/price.json?date={date}&hour={hour}"
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()  # Parse the JSON response

            # Insert the data into the database -- datetime format:  "2022-11-14THH:00:00.000Z"
            await porssisahko_repository.insert_entry(data["price"], f"{date}T{hour:02d}:00.000Z")

        print(f"Missing data successfully inserted into the database.")
    except requests.RequestException as e:
        print(f"Error fetching data from the API: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# we need a wrapper to run the async task in a synchronous context
def fetch_and_insert_porssisahko_data_sync():
    asyncio.run(fetch_and_insert_porssisahko_data())

def fetch_and_insert_missing_porssisahko_data_sync(start_datetime_str: str):
    asyncio.run(fetch_and_insert_missing_porssisahko_data(start_datetime_str))


# Set up the scheduler
ps_scheduler = BackgroundScheduler()
# Trigger to run the task every day at 14:15
ps_trigger = CronTrigger(hour=14, minute=15)

# NOTE DEBUG: For debugging/testing purposes, you can use an interval trigger to run every 15 seconds or so
#ps_trigger = IntervalTrigger(seconds=10)

ps_scheduler.add_job(fetch_and_insert_porssisahko_data_sync, ps_trigger)
ps_scheduler.start()

# Ensure the scheduler shuts down properly on application exit
def shutdown_scheduler():
    print("Shutting down scheduler...")
    ps_scheduler.shutdown()

