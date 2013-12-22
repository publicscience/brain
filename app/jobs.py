from app import brain
import schedule
import time, threading

# Logging
from app.logger import logger
logger = logger(__name__)
logger.info('Scheduling jobs...')

"""
Fetch tweets and memorize and process them
every hour.
"""
schedule.every().hour.do(brain.ponder)

"""
Every 10 minutes consider tweeting something poignant.
"""
schedule.every(10).minutes.do(brain.consider)

# Run the jobs without blocking the main thread.
# http://bit.ly/19V6qTF
cease_continuous_run = threading.Event()

class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):
        while not cease_continuous_run.is_set():
            schedule.default_scheduler.run_pending()
            time.sleep(1)

continuous_thread = ScheduleThread()
continuous_thread.daemon=True # kills thread when main process ends.
continuous_thread.start()
