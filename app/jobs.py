from app import brain
import schedule
import time

"""
Fetch tweets and memorize and process them
every hour.
"""
schedule.every().hour.do(brain.ponder)

"""
Every 10 minutes consider tweeting something poignant.
"""
schedule.every(10).minutes.do(brain.consider)

# Run the jobs.
while True:
    schedule.run_pending()
    time.sleep(1)
