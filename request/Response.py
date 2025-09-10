from pydantic import BaseModel

class PostSummary(BaseModel):
    is_ai_post: bool
    title: str
    summary: str
    highlights: str
    hashtag: str