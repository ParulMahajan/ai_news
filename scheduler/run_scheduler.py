import time
import schedule

from utils.db import delete_old_history_from_db
from utils.logger import logger
from core.parser import process_news_feeds


def run_job():
    try:

        logger.info("Starting job news feed")
        process_news_feeds()
        logger.info("Job completed successfully")
    except Exception as e:
        logger.error(f"Error running job: {str(e)}")

def run_delete_history():
    try:
        logger.info("Running delete_old_history_from_db")
        delete_old_history_from_db()
        logger.info("Delete history completed successfully")
    except Exception as e:
        logger.error(f"Error deleting history: {str(e)}")

def main():

    logger.info("Starting scheduler")
    schedule.every(5).minutes.do(run_job)

    # Run once immediately on startup
    run_job()

    # Schedule delete history (12AM and 12PM)
    schedule.every().day.at("00:00").do(run_delete_history)
    schedule.every().day.at("12:00").do(run_delete_history)


    while True:
        schedule.run_pending()
        time.sleep(1)
