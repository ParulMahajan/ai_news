from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate

ai_title_check = PromptTemplate.from_template(
    template=(
        "Evaluate the following blog post title and respond with 'Yes' or 'No' based on these criteria:\n\n"
        "1. The title announces a new innovation or catchy change/development in AI technology that will attract tech-savvy audience.\n"
        "2. The change/development is introduced by a reputable organization (e.g. Anthropic, OpenAI, Google, Meta, Microsoft, AWS or any prominent LLM provider).\n\n"
        "Respond with No, If the title pertains to a job posting, tutorial, opinion piece, or lacks association with a recognized organization.\n\n"
        "Title: {title}"
    )
)

summary_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are an AI assistant specializing in summarizing AI technology articles for a tech-savvy audience. "
                    "Analyze the following content. "
                    "If it discusses a new innovation or significant development in AI technology by a reputable organization (e.g., OpenAI, Google, Meta,anthropic, Microsoft, AWS or any prominent LLM provider), "
                    "provide:\n"
                    "1. A compelling and catchy TITLE suitable for instagram/facebook post.\n"
                    "2. A SUMMARY highlighting in maximum 3-5 key points(each key point separated by new empty line). Ensure the summary is informative, engaging, and tailored.\n"
                    "3. An IMAGE_TEXT section:\n"
                    "   - HEADLINE: a shorter, punchy version of the title (max 10 words).\n"
                    "   - HIGHLIGHTS: 3–5 bullet-style phrases (max 6 words each) suitable for overlaying on an image.\n"
                    "   - The text should be short, bold, and impactful, designed to catch attention in a quick scroll.\n\n"

                    "If the content is a job posting, opinion piece, or not related to a notable AI innovation, respond with 'NO'.\n\n"

                    "Strictly Format the response as:"
                    "TITLE: <new title>\n"
                    "||| \n"
                    "SUMMARY:\n"
                    "<summary points>\n"
                    "||| \n"
                    "IMAGE_TEXT:\n"
                    "HEADLINE: <short headline> !!!\n"
                    "HIGHLIGHTS:\n"
                    "- <highlight 1>\n"
                    "- <highlight 2>\n"
                    "- <highlight 3>\n"
                    "- <highlight 4>\n"
                    "- <highlight 5>"
        ),
        ("human", "{content}"),
    ]
)


post_image = PromptTemplate.from_template(
    template=(
        """
Create a high-resolution, realistic portrait image with subtle stylish animations, designed for a professional tech-savvy social media audience. The image should visually represent the essence of the given article’s title and summary in a polished, contemporary style.

Specifications:
1. **Top 10% Overlay:** A translucent dark overlay with the articl'e title in bold, clean, modern typography (sans-serif). The overlay should blend smoothly with the background but maintain strong readability.

2. **Background:** The background should depict a refined, professional, tech-inspired environment with natural lighting and a polished color palette, adding sophistication without distracting from the main subject.

3. **Foreground Infographic Elements:** The article’s **highlights** will be prominently displayed as large, crystal-clear infographic elements.  
   - Each highlight should be paired with a simple, professional icon (e.g., book, graduation cap, handshake, AI chip).  
   - The text must use modern, sharp sans-serif fonts in pure white (or dark over light background) for maximum readability.  
   - Highlights should be **brief and error-free** (correct spellings: “OpenAI Learning Accelerator Launched”, “500K ChatGPT Licenses Distributed”, “Partnerships with IIT Madras, AICTE”, “Training for AI Literacy”, “Nurturing the Next Generation of Learners”).  
   - Position highlights evenly across the foreground, with enough spacing to avoid clutter. Each should look like a “callout card” or infographic bubble.

4. **Depth of Field:** Subtle depth of field (soft bokeh background) so the portrait and highlight elements remain in crisp focus.

5. **Mood:** The overall mood should be sophisticated, innovative, and professional, reflecting the dynamic nature of technology.
 
Article Information:

Title: {headline}\n
Summary: \n{summary}\n
Highlights: {highlights}\n"""
    )
)



