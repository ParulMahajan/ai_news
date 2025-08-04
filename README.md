# 🤖 AI-Powered Social Media Auto-Poster

This application automates the process of posting AI-related articles to **Facebook**, **Instagram**, and **LinkedIn**. It leverages RSS feeds, a Large Language Model (LLM), and image generation to create and distribute professional content effortlessly.

---

## 🌐 My Pages

- **Facebook**: [facebook.com/profile.php?id=61575680777885](https://www.facebook.com/profile.php?id=61575680777885)
- **Instagram**: [instagram.com/ainewsss](https://www.instagram.com/ainewsss)
- **LinkedIn**: [linkedin.com/company/ai-newsss](https://www.linkedin.com/company/ai-newsss/?viewAsMember=true)

---

## 🚀 Features

- Automatically fetches RSS feed articles.
- Uses LLM to:
  - Filter for AI-related topics.
  - Generate a new title and summary.
  - Create an AI-generated image for the post.
- Posts the final content (title, summary, image) to:
  - Facebook
  - Instagram
  - LinkedIn

---

## 🧭 How It Works

1. **Fetch RSS Feeds**
   - Reads RSS feed URLs from a MySQL database.
   - Fetches the latest 5 articles from each active feed.

2. **LLM Filtering & Content Generation**
   - Sends the article title to the LLM to determine AI relevance.
   - If relevant, sends the full article body to the LLM to generate a new:
     - Title
     - Summary
   - Sends the above to another LLM call to generate an image.

3. **Post to Social Media**
   - Automatically posts the title, summary, and generated image to Facebook, Instagram, and LinkedIn.

---

## 🛠️ Requirements

### 🔸 MySQL Database

#### Tables

```sql
CREATE TABLE ai_feeds.rss_feeds (
  id INT NOT NULL AUTO_INCREMENT,
  feed_url VARCHAR(255) NOT NULL,
  is_active TINYINT(1) DEFAULT NULL,
  PRIMARY KEY (id)
);
```

```sql
CREATE TABLE ai_feeds.post_history (
  id INT NOT NULL AUTO_INCREMENT,
  post_id VARCHAR(255) NOT NULL,
  feed_url VARCHAR(255) NOT NULL,
  published TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (id)
);
```

#### Sample Feed Insert

```sql
INSERT INTO rss_feeds (feed_url)
VALUES ('https://hnrss.org/newest?q=AI');
```

#### Environment Variables

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_DATABASE=ai_feeds
```

---

### 🔸 Facebook & Instagram Configuration

You need a Facebook developer account and an Instagram Business account.

```env
FB_PAGE_ID=
FB_APP_ID=
FB_APP_SECRET=
FB_ACCESS_TOKEN=
FB_PROFILE_LINK=
IG_ACCOUNT_ID=
IG_PROFILE_LINK=
```

---

### 🔸 LinkedIn Configuration

You need a LinkedIn developer account.

```env
LINKEDIN_ACCESS_TOKEN=
LINKEDIN_REFRESH_TOKEN=
LN_PAGE_ID=
LN_PROFILE_LINK=
```



### 🔸 LLM and Debugging Configuration

Add the following environment variables to enable LLM processing and logging:

```env
# OpenAI API key for LLM calls
OPENAI_API_KEY=

# Logging and tokenizer settings
LOG_LEVEL=DEBUG
TOKENIZERS_PARALLELISM=false

# Optional: Langsmith tracing and debugging
LANGSMITH_API_KEY=
LANGSMITH_ENDPOINT=
LANGSMITH_PROJECT=
LANGSMITH_TRACING=true
```
---

## 📌 Notes

- Ensure RSS feeds are valid and support full-text content.
- LLM models should be configured to handle:
  - Relevance classification
  - Title & summary generation
  - Image prompt generation
- Handle access token refreshes and rate limits for social media APIs.
- Consider logging or notifications for failed posts.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

## 📬 Contact

For support or business inquiries, please reach out via GitHub Issues or email.




