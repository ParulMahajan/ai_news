import datetime
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Function to get the MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),         # Your MySQL host
        user=os.getenv("DB_USER"),              # Your MySQL user
        password=os.getenv("DB_PASSWORD"),      # Your MySQL password
        database=os.getenv("DB_DATABASE")       # The database with the RSS URLs
    )

# Function to retrieve all feed URLs from the MySQL database
def get_feed_urls_from_db(connection):

    cursor = connection.cursor()
    cursor.execute("SELECT feed_url FROM rss_feeds where is_active=1")
    feed_urls = cursor.fetchall()
    cursor.close()
    return [url[0] for url in feed_urls]

# Function to retrieve all feed URLs from the MySQL database
def get_post_history_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT post_id FROM post_history")
    post_ids = cursor.fetchall()
    cursor.close()
    return [id[0] for id in post_ids]

def save_post_history_to_db(post_id, feed_url,published, connection):

    # Parse the published string to a datetime object
    published_dt = datetime.datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")

    cursor = connection.cursor()
    cursor.execute("INSERT INTO ai_feeds.post_history (post_id, feed_url,published) VALUES (%s, %s, %s)", (post_id, feed_url,published_dt))
    connection.commit()
    cursor.close()


# dd=get_mysql_connection()
# print(dd)