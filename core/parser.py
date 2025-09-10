import feedparser

from client.google import generate_image
from social.social_media_helper import post_to_social_media
from model.chain import summary_chain, title_check_chain, image_prompt_chain

from client.newspaper3k import fetch_article_content
from utils.db import get_feed_urls_from_db, get_mysql_connection, get_post_history_from_db, save_post_history_to_db
from utils.logger import logger


def process_news_feeds():
    connection = get_mysql_connection()

    # Define a list to collect new post history records
    new_post_history: list[tuple[str, str, str]] = []

    feed_urls = get_feed_urls_from_db(connection)
    post_id_history_list = set(get_post_history_from_db(connection))

    for feed_url in feed_urls:
        logger.info("\n")
        logger.info(f"Fetching articles from: {feed_url}")
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:10]:  # Limit to the first 5 entries
            try:
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
                ai = summary_chain.invoke({"content": article_text})
                # print(f"Summary: {summary.content}")
                if str(ai.is_ai_post).strip().lower() in ("no","false") :
                    logger.debug(f"Skipped: not AI-related POST")
                    new_post_history.append((entry.id, feed_url, entry.published))
                    continue

                ai_title = ai.title
                logger.info("\nAI Title: " + ai_title)
                ai_summary = ai.summary
                logger.info("AI Summary: \n" + ai_summary)
                ai_image_highlights = ai.highlights
                logger.info("AI Image Highlights: \n" + ai_image_highlights)
                ai_hashtag = ai.hashtag + " #AIGenerated #CreatedWithAI"

                # generate image prompt
                image_prompt = image_prompt_chain.invoke({"title":ai_title,"highlights":ai_image_highlights})
                logger.info(f"\nimage prompt:\n {image_prompt.content}")

                # generate llm image
                image_bytes = generate_image(image_prompt.content)
                if image_bytes:
                    result = post_to_social_media(title=ai_title, summary=ai_summary, image_bytes=image_bytes,hashtag=ai_hashtag)
                    logger.debug(f"Posted to social media : {result}")

                    # Save the new post ID to the list, so we can skip it next time
                    new_post_history.append((entry.id, feed_url, entry.published))
            except Exception as e:
                logger.error(f"Error processing feeds: {str(e)}")

    # Save the new post history to the database
    for post_id, feed_url, published in new_post_history:
        save_post_history_to_db(post_id, feed_url, published, connection)

if __name__ == "__main__":
    process_news_feeds()
