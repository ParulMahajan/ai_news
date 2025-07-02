from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate

ai_title_check = PromptTemplate.from_template(
    template=(
        "Evaluate the following blog post title and respond with 'Yes' or 'No' based on these criteria:\n\n"
        "1. The title announces a new innovation and catchy change/development in AI technology that will attract tech-savvy audience.\n"
        "2. The change/development is introduced by a reputable organization (e.g. Anthropic, OpenAI, Google, Meta, Microsoft, AWS or any prominent LLM provider).\n\n"
        "Respond with No, If the title pertains to a job posting, tutorial, opinion piece, or lacks association with a recognized organization.\n\n"
        "Title: {title}"
    )
)

summary_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="You are an AI assistant specializing in summarizing AI technology articles for a tech-savvy audience. Analyze the following content. "
                    "If it discusses a new innovation or significant development in AI technology by a reputable organization (e.g., OpenAI, Google, Meta,anthropic, Microsoft, AWS or any prominent LLM provider), "
                    "provide:"
                    "- A compelling and catchy caption suitable for instagram/facebook post."
                    "- A concise summary highlighting maximum 3-5 key points and each key point separated by new empty line."
                    "- Ensure the summary is informative, engaging, and tailored for readers interested in cutting-edge AI developments."
                    "If the content is a job posting, opinion piece, or not related to a notable AI innovation, respond with 'NO'."

                    "Format the response as:"
                    "TITLE: <new title>  |||" 
                    "SUMMARY:"
                    "<summary points>"),
        ("human", "{content}"),
    ]
)

post_image = PromptTemplate.from_template(
    template=(
        "Create a high-quality, realistic image suitable for a professional social media post, "
        "based on the following AI news article:\n\n"
        "Title: {titleData}\n"
        "Summary: {summaryData}\n\n"

        "Image Requirements:\n"
        "1. The image must clearly and realistically depict the main concept or event in the article.\n"
        "2. Focus on the specific AI technology, application, or industry mentioned.\n"
        "3. Use real-world settings, objects, or people to tell the story visually.\n"
        "4. Avoid abstract symbols like random circuits, floating icons, or generic network graphics.\n"
        "5. Do not use any visible text or words in the image. No captions, banners or text overlays. Only visual elements like objects, symbols, or logos are allowed. Use icons or imagery to convey meaning instead of written language..\n"
        "6. Keep the image clean and informative. It should visually tell the story without needing extra explanation.\n"
        "7. Use professional-quality lighting, framing, and a realistic documentary/editorial photography style.\n"
        "8. Use a natural and context-appropriate color palette."
    )
)
