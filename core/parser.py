import feedparser
from social.social_media_helper import post_to_social_media
from model.chain import summary_chain, title_check_chain
from model.llm import llm_dalle, google_client
from model.prompt.customPrompt import post_image
from utils.post_reader import fetch_article_content
from utils.db import get_feed_urls_from_db, get_mysql_connection, get_post_history_from_db, save_post_history_to_db
from utils.logger import logger
from PIL import Image
from io import BytesIO

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
                summary_resp = summary_chain.invoke({"content": article_text})
                # print(f"Summary: {summary.content}")
                if str(summary_resp.content).strip().lower() == "no":
                    logger.debug(f"Skipped: not AI-related POST")
                    new_post_history.append((entry.id, feed_url, entry.published))
                    continue

                ai = parse_summary_response(summary_resp.content)
                ai_title = ai["title"]
                ai_summary = ai["summary"]
                ai_image_headline = ai["image_headline"]
                ai_image_highlights = ai["image_highlights"]

                # generate llm image
                image_prompt = post_image.format(headline=ai_title, summary=ai_summary,
                                                 highlights=ai_image_highlights)
                # ai_image_url = llm_dalle.run(image_prompt)
                response = google_client.models.generate_content(
                    model="gemini-2.5-flash-image-preview",
                    contents=[image_prompt],
                )

                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        logger.info(part.text)
                    elif part.inline_data is not None:
                        # Open image from binary data
                        ai_image = Image.open(BytesIO(part.inline_data.data))
                        # Save locally if needed
                        ai_image.save("generated_image.jpeg")

                        # Convert PIL Image to raw bytes for direct use
                        buf = BytesIO()
                        ai_image.save(buf, format="PNG")  # or "JPEG"
                        image_bytes = buf.getvalue()

                        # image = "/Users/pmahajan/Desktop/personal_git_projects/ai_news/generated_image.jpeg"
                        # # Read the image file as raw bytes
                        # with open(image, "rb") as image_file:
                        #     image_bytes = image_file.read()

                        # Now image_bytes can be passed to your posting function
                        if image_bytes:
                            logger.info("ai_image generated and converted to bytes")
                            #result = "test"
                            result = post_to_social_media(title=ai_title, summary=ai_summary, image_bytes=image_bytes)
                            logger.debug(f"Posted to socialmedia : {result}")
                            # Save the new post ID to the list, so we can skip it next time
                            new_post_history.append((entry.id, feed_url, entry.published))
            except Exception as e:
                logger.error(f"Error processing feeds: {str(e)}")



    # Save the new post history to the database
    for post_id, feed_url, published in new_post_history:
        save_post_history_to_db(post_id, feed_url, published, connection)


def parse_summary_response(response_content: str):
    """
    Parse the AI response into structured components:
    - new_title: str
    - summary_text: str
    - image_headline: str
    - image_highlight_list: list[str]
    """

    # Split the response into title, summary, and image_text
    title, summary, image_text = response_content.split("|||")

    # Clean title
    new_title = title.replace("TITLE:", "").strip()

    # Clean summary
    summary_text = summary.replace("SUMMARY:", "").strip()

    # Process IMAGE_TEXT
    image_text = image_text.replace("IMAGE_TEXT:", "").strip()
    headline, highlights = image_text.split("!!!")

    # Clean headline
    headline = headline.replace("HEADLINE:", "").strip()

    # Clean highlights
    highlights_text = highlights.replace("HIGHLIGHTS:", "").strip()
    highlight_list = [
        line.lstrip("-").strip()
        for line in highlights_text.splitlines()
        if line.strip().startswith("-")
    ]
    # Format as a multiline string with hyphens
    formatted_highlights = "\n" + "\n".join(f"- {item}" for item in highlight_list)

    logger.info(f"ai_title: {new_title}")
    logger.info(f"ai_summary: {summary_text}")
    logger.info(f"ai_headline: {headline}")
    logger.info(f"ai_highlights: {formatted_highlights}")
    return {
        "title": new_title,
        "summary": summary_text,
        "image_headline": headline,
        "image_highlights": formatted_highlights,
    }



if __name__ == "__main__":
    process_news_feeds()
