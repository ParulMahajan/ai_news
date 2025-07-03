import schedule
import time

from utils.db import delete_old_history_from_db

# Schedule the job at 12:00 PM and 12:00 AM
schedule.every().day.at("00:00").do(delete_old_history_from_db)
schedule.every().day.at("12:00").do(delete_old_history_from_db)

while True:
    schedule.run_pending()
    time.sleep(60)