import boto3
import os
from datetime import datetime, timezone, timedelta
from dateutil import parser
from utils.logger import logger as log
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

IS_LOCAL = os.getenv("LOCAL_DYNAMO", "false").lower() == "true"
AWS_PROFILE = os.getenv("AWS_PROFILE")

# Initialize DynamoDB client
if IS_LOCAL:
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="ap-southeast-1",
        endpoint_url="http://localhost:8000",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy"
    )
else:
    session = boto3.Session(profile_name=AWS_PROFILE) if AWS_PROFILE else boto3.Session()
    dynamodb = session.resource("dynamodb", region_name="ap-southeast-1")

# Table references
rss_table = dynamodb.Table("rss_feeds")
history_table = dynamodb.Table("post_history")

def get_feed_urls_from_db():
    """Fetch all active feed URLs from DynamoDB rss_feeds table"""
    try:
        response = rss_table.scan(
            FilterExpression="is_active = :val",
            ExpressionAttributeValues={":val": True}
        )
        feeds = [item['feed_url'] for item in response.get('Items', [])]
        return feeds
    except Exception as e:
        log.error(f"Error fetching feeds: {e}")
        return []

def get_post_history_from_db():
    """Fetch all post_ids from DynamoDB post_history table"""
    try:
        response = history_table.scan(ProjectionExpression="post_id")
        post_ids = [item['post_id'] for item in response.get('Items', [])]
        return post_ids
    except Exception as e:
        log.error(f"Error fetching post history: {e}")
        return []

def save_post_history_to_db(recent_posts):
    try:
        with history_table.batch_writer() as batch:
            for post_id, feed_url, published, is_posted in recent_posts:
                try:
                    published_dt = parser.parse(published)
                except Exception:
                    log.warn("error when converting date")
                    published_dt = datetime.now(timezone.utc)

                batch.put_item(
                    Item={
                        'post_id': post_id,
                        'feed_url': feed_url,
                        'published': published_dt.isoformat(),
                        'created_at': datetime.now(timezone(timedelta(hours=7))).isoformat(),
                        'is_posted': is_posted
                    }
                )
        log.info(f"Batch saved {len(recent_posts)} post history records")
    except Exception as e:
        log.error(f"Error batch saving post history: {e}")

def delete_old_history_from_db(days=30):
    """Delete entries older than given days using batch operations"""
    try:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        response = history_table.scan()

        items_to_delete = []
        for item in response.get('Items', []):
            try:
                item_date = parser.parse(item['published'])
                if item_date.tzinfo is None:
                    item_date = item_date.replace(tzinfo=timezone.utc)
                if item_date < cutoff_date:
                    items_to_delete.append(item['post_id'])
            except Exception as e:
                log.error(f"Error while doing date conversion for delete: {e}")
                continue

        if items_to_delete:
            with history_table.batch_writer() as batch:
                for post_id in items_to_delete:
                    batch.delete_item(Key={'post_id': post_id})

            log.info(f"Batch deleted {len(items_to_delete)} history records older than {days} days.")
        else:
            log.info(f"No records found older than {days} days.")

    except Exception as e:
        log.error(f"Error batch deleting old history: {e}")
