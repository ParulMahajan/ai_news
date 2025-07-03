import os
import sys
from utils.logger import logger
from dotenv import load_dotenv
load_dotenv()
from scheduler.run_scheduler import main as scheduler_main


def main():
    try:
        logger.info("Starting News Feed Application")
        scheduler_main()

    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure working directory is project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    main()