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

    (
        "system",
        "Expert AI infographic prompt-designer for tech news. "
        "Non-negotiables: "
        "(1) Ultra High Definition, perfectly spelled, readable text; "
        "(2) solid, high-contrast highlight panels (NO translucency); "
        "(3) background visuals derived ONLY from the Article; "
        "(4) cards never overlap the subject; "
        "(5) no duplicated or invented text. Render all text as clean vector typography."
    ),
    (
        "human",
        """
Return ONE final image-generation prompt. Use the exact strings from the Article's Title and Highlights appended below.
Do not paraphrase. Keep instructions short and directive.

— Title (fixed size = 20% of canvas height) —
• Render the Article's Title exactly as written (no changes).
• Top-center, bold sans-serif, 1–2 lines, auto-scale to occupy exactly 20% of canvas height.
• Strong contrast.
• Hard negatives: no curvature/tilt, no 3D/extrusion, no extra characters.

— Background (strictly from the Article) —
• Derive ALL visuals from the Article's Title & Highlights (entities, application/company logos, utilities, objects, places, actions, themes).
• Create a sophisticated, professional background scene that reflects the article's story in the background.
• Keep secondary; add soft vignette/blur behind text zones; maintain foreground → midground → background depth.

— Highlights (exact count, big, solid) —
• Use exactly the Article's Highlights — no duplicates, omissions, or rewording.
• Create opaque cards (rect or rounded).
• Card grid & size preset (apply strictly):
  – Place cards outside the subject's bounding box. 
  – Card height ≈ 25% of canvas height.
• Typography fit (strict):
  – Text fills 85–95% of card width and 70–80% of card height (≤3 lines; natural wraps).
  – Minimum font size ≥ 120 px at 1080-px canvas (scale proportionally). If smaller, enlarge the card.
  – High contrast; padding ≥ 28 px; line-height 1.18–1.26.
• Icons optional and small (≤ 15% of card height); text remains dominant.
• Space guard: if free space around cards > 10% vertically/horizontally, increase card and font size until constraints are met.

— Composition & Quality —
• Foreground: title + highlight cards (primary). Midground: subject derived from the Article. Background: thematic ambience.
• Even, soft lighting on text zones. Validate: no misspelling, truncation, duplication, overlap, or background words.
• Aspect ratio: square or 4:5. Editorial, mobile-readable.

---
**Article Information**
Title: {title}  
Highlights: {highlights}

Return only the final descriptive image prompt suitable for an image-generation model.
"""
    )
])
# in the lower third
# – Use a tidy grid occupying 90% of canvas width with equal columns and gaps ≈ 3% of canvas width.
#• Cards stay horizontal; equal gaps; no overlap with the subject.