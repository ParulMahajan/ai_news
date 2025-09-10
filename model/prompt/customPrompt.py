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

summary_prompt = ChatPromptTemplate.from_messages([
    ("system","You are an AI assistant specializing in summarizing AI technology articles for a tech-savvy audience"),
    ("human","""
Follow the following instructions and analyze the below mentioned content:

If it discusses a new innovation or significant development in AI technology by a reputable organization (e.g., OpenAI, Google, Meta, anthropic, Microsoft, AWS or any prominent LLM provider),
provide the following:
1. A compelling and catchy TITLE explaining the article and the suitable for social media post.
2. A SUMMARY highlighting in maximum 3-5 key points (each key point separated by new empty line). Ensure the summary is informative, engaging, and tailored.
3. Hashtags: Generate relevant 2-4 hashtags related to AI technology, organization etc. mentioned in the article, ensuring they are popular and widely used on social media platforms.
4. Highlight points(bullet-style phrases, max 6-8 words each) for each of the summary points, suitable for overlaying as infographic elements on the image. The text should be short, bold, and impactful, designed to catch attention in a quick scroll. For the highlights field, output them as a numbered list. 
Each item must:
- start with the number and a period (e.g., 1. 2. 3.)
- wrap the text in double quotes (" ")

Example:
1. "AWS targets 20% growth by 2025"
2. "Anthropic's revenue soared 5x"


If the content is a job posting, opinion piece, or not related to a notable AI innovation, respond is_ai_post with 'NO'.

Content: {content}
""")
])

# Prompt for generating image instructions dynamically
create_image_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert prompt engineer for AI image generation."),
    ("human", """
Always include these fixed visual guidelines: 
- Make sure there are no text mistakes on the image 
- Dynamic title overlay with bold sans-serif typography 
- Image background: explaining about the article 
- Professional infographic cards for foreground highlights. Ensure each is distinct, do not duplicate and accurately transcribed. It should be easily readable. 
- Strictly focus on Title's and Highlight's text should have correct spelling. 

Your task: 
1. Read the article title and highlights. 
2. Reframe the above guidelines into a single professional AI image generation prompt. 
3. Return only the final image prompt.

Article Information
Title: {title}
Highlights: {highlights}
""")
])
