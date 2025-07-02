import feedparser
from social.social_media_helper import post_to_social_media
from model.chain import summary_chain, title_check_chain
from model.llm import llm_dalle
from model.prompt.customPrompt import post_image
from utils.post_reader import fetch_article_content
from utils.db import get_feed_urls_from_db, get_mysql_connection, get_post_history_from_db, save_post_history_to_db
from utils.logger import logger

def process_news_feeds():
    connection = get_mysql_connection()
    feed_urls = get_feed_urls_from_db(connection)
    post_id_history_list = get_post_history_from_db(connection)

    # Define a list to collect new post history records
    new_post_history = []

    try:
        for feed_url in feed_urls:
            logger.info("\n")
            logger.info(f"Fetching articles from: {feed_url}")
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:  # Limit to the first 5 entries
                logger.info("\n")
                logger.info(f"Title: {entry.title}")
                logger.info(f"ID: {entry.id}, Published: {entry.published}")
                logger.info(f"Link: {entry.link}")

                # Check if the post ID already exists in the database
                if entry.id in post_id_history_list:
                    logger.info(f"Skipped: already posted/checked")
                    continue

                # Check if the title is related to AI
                is_AI_title = title_check_chain.invoke({"title": entry.title})
                if str(is_AI_title.content).strip().lower() == "no":
                    logger.debug(f"Skipped: not AI-related")
                    new_post_history.append((entry.id, feed_url, entry.published))
                    continue

                # Fetch article content using Newspaper3k
                try:
                    article_content = fetch_article_content(entry.link)
                    article_text = article_content.get('text', '').strip()
                    article_image = article_content.get('image', '')  # Get the main image URL
                except Exception as e:
                    logger.error(f"Skipped (download error)")
                    new_post_history.append((entry.id, feed_url, entry.published))
                    continue

                # Skip if article text is too short (e.g., less than 100 chars)
                if not article_text or len(article_text) < 100:
                    logger.error(f"Skipped (content too short): {entry.link}")
                    new_post_history.append((entry.id, feed_url, entry.published))
                    continue

                # call LLM to generate summary
                response = summary_chain.invoke({"content": article_text})
                #print(f"Summary: {summary.content}")
                if str(response.content).strip().lower() == "no":
                    logger.debug(f"Skipped: not AI-related POST")
                    new_post_history.append((entry.id, feed_url, entry.published))
                    continue

                # Split the response into title and summary
                title, summary = response.content.split("|||")
                new_title = title.replace("TITLE:", "").strip()
                summary_text = summary.replace("SUMMARY:", "").strip()

                # Save the new post ID to the list, so we can skip it next time
                new_post_history.append((entry.id, feed_url, entry.published))

                # generate llm image
                # image_prompt = post_image.format(summaryData=summary_text, titleData=new_title)
                # ai_image_url = llm_dalle.run(image_prompt)

                # if  ai_image_url :
                #     article_image = ai_image_url

                logger.info(f"new_title: {new_title}")
                logger.info(f"summary: {summary_text}")
                logger.info(f"imageUrl: {article_image}")
                result = "test"
                #result = post_to_social_media(title=new_title, summary=summary_text,image_url=article_image)
                logger.debug(f"Posted to Facebook: {result}")

                #logger.info("\n")

        # Save the new post history to the database
        for post_id, feed_url, published in new_post_history:
            save_post_history_to_db(post_id, feed_url, published, connection)

    finally:
        connection.close()


if __name__ == "__main__":
    process_news_feeds()
