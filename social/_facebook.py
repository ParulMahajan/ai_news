from facebook import  GraphAPI,GraphAPIError
from utils.logger import logger
import os
import re

access_token = os.getenv("FB_ACCESS_TOKEN")
graph = GraphAPI(access_token)

ig_profile_link = os.getenv("IG_PROFILE_LINK")
ig_link = f"📸 Instagram: {ig_profile_link}"

ln_profile_link = os.getenv("LN_PROFILE_LINK")
ln_link = f"🔗 LinkedIn: {ln_profile_link}"

def post_to_facebook(temp_path, title, summary, hashtag):

    try:
        formatted_message = format_post_content(title, summary)
        with open(temp_path, 'rb') as image_file:
            result = graph.put_photo(
                image=image_file,
                message=formatted_message + "\n\n" + ig_link + "\n\n" + ln_link + "\n\n" + hashtag,
                published=True
            )
            post_id = result["post_id"]
            if post_id:
                graph.put_object(
                    parent_object=post_id,
                    connection_name="comments",
                    message=summary
                )

            return result
    except GraphAPIError as e:
        logger.error(f"Facebook GraphAPIError error: {str(e)}")

    except Exception as e:
        logger.error(f"Facebook posting failed: {e}")

def format_post_content(title, summary):

    lines = summary.strip().splitlines()
    first_summary_point = next(line.strip() for line in lines if line.strip())
    first_summary_point = re.sub(r'^[^\w]+', '', first_summary_point).strip()
    comment_text = "For full article details, check the comment section..."
    # Add CTA (Call to Action)
    cta = "🔔 Follow us for daily AI updates!"
    separator = "\n \n"
    return f"{first_summary_point}\n\n{comment_text}{separator}\n\n{cta}"

def get_long_lived_token():
    """Convert short-lived token to long-lived token"""
    app_id = os.getenv("FB_APP_ID")
    app_secret = os.getenv("FB_APP_SECRET")
    short_lived_token = os.getenv("FB_ACCESS_TOKEN")

    graph = GraphAPI(access_token=short_lived_token,version="3.1")
    try:
        # Exchange tokens using the correct endpoint
        response = graph.extend_access_token(app_id, app_secret)
        return response['access_token']
    except GraphAPIError as e:
        print(f"Error exchanging token: {e}")
        return None

def get_permanent_page_token():
    """Get permanent page access token"""
    user_token = get_long_lived_token()
    if not user_token:
        return None
    graph = GraphAPI(user_token, version="3.1")
    page_id = os.getenv("FB_PAGE_ID")
    try:
        pages = graph.get_object('me/accounts')
        for page in pages['data']:
            if page['id'] == page_id:
                return page['access_token']
        return None
    except GraphAPIError as e:
        print(f"Error getting page token: {e}")
        return None


def delete_all_posts():
    """Delete all posts from the Facebook page"""
    access_token = os.getenv("FB_ACCESS_TOKEN")
    page_id = os.getenv("FB_PAGE_ID")
    graph = GraphAPI(access_token)

    try:
        # Get posts in batches of 100
        while True:
            # Get posts from the page
            posts = graph.get_object(
                f"{page_id}/posts",
                fields="id",
                limit=100
            )

            if not posts['data']:
                logger.info("No more posts to delete")
                break

            # Delete each post
            for post in posts['data']:
                try:
                    graph.delete_object(post['id'])
                    logger.info(f"Deleted post {post['id']}")
                except GraphAPIError as e:
                    logger.error(f"Error deleting post {post['id']}: {str(e)}")
                    continue

    except GraphAPIError as e:
        logger.error(f"Error fetching posts: {str(e)}")
        return False

    return True

# permToken = get_permanent_page_token()
# print(f"Permanent Page Token: {permToken}")
# delete_all_posts()