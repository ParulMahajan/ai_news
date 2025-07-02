from newspaper import Article
import requests

# Function to fetch article content from the URL using newspaper3k
def fetch_article_content(url: str):
    article = Article(url)
    article.keep_article_html = True
    article.download()
    article.parse()

    # Save the raw HTML to a file
    # with open("article.html", "w", encoding="utf-8") as file:
    #     file.write(article.html)

    return {
        "text": article.text,  # Extracted article content
        "image": article.top_image  # Extracted main image URL
    }  # Extracted article content


# Write article data to a text file
def write_to_file(article_data):
    with open("articles_output.txt", "a") as file:
        file.write(f"Article Content: \n{article_data['text']}...\n\n")  # Write the first 500 characters of the article