import os
import sys

from client.aws_dynamodb import delete_old_history_from_db
from core.parser import process_news_feeds
from utils.logger import logger
from dotenv import load_dotenv
load_dotenv()
from scheduler.run_scheduler import main as scheduler_main


def main():
    try:
        logger.info("Starting News Feed Application")
        #scheduler_main()
        process_news_feeds()
        delete_old_history_from_db()
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        sys.exit(1)

def lambda_handler(event=None, context=None):
    """Lambda entry point (AWS invokes this)."""
    logger.info("Starting News Feed Application (Lambda)")
    try:
        process_news_feeds()
        delete_old_history_from_db()
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Ensure working directory is project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    main()