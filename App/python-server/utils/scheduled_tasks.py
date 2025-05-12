import asyncio
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from utils.porssisahko_tools import insert_into_porssisahko_table

# The task to fetch data and insert it into the database
def fetch_and_insert_porssisahko_data():
    try:
        # Fetch data from the API
        response = requests.get("https://api.porssisahko.net/v1/latest-prices.json")
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response
        # Insert the data into the database using the async function
        asyncio.run(insert_into_porssisahko_table(data["prices"]))

        print(f"Data successfully inserted at {datetime.now()}")
    except requests.RequestException as e:
        print(f"Error fetching data from the API: {e}")
    except Exception as e:
        print(f"Non-API error: {e}")

# Set up the scheduler
scheduler = BackgroundScheduler()
# trigger always 14.15
trigger = CronTrigger(hour=14, minute=15)
# NOTE: For debugging/testing purposes, you can 
# use an interval trigger to run every 15 seconds or so
#trigger = IntervalTrigger(seconds=15)
scheduler.add_job(fetch_and_insert_porssisahko_data, trigger)
scheduler.start()

# Ensure the scheduler shuts down properly on application exit
def shutdown_scheduler():
    scheduler.shutdown()

# TODO: implement a task to see if there are missing entries in the database
# between two dates, and if so, fetch them from the API and insert them into the database
