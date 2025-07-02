import time
import schedule
from utils.logger import logger
from core.parser import process_news_feeds
from dotenv import load_dotenv

def run_job():
    try:
        load_dotenv()
        logger.info("Starting job news feed")
        process_news_feeds()
        logger.info("Job completed successfully")
    except Exception as e:
        logger.error(f"Error running job: {str(e)}")

def main():
    logger.info("Starting scheduler")
    schedule.every(5).minutes.do(run_job)

    # Run once immediately on startup
    run_job()

    while True:
        schedule.run_pending()
        time.sleep(1)
