from langchain.chat_models import init_chat_model
from google import genai
import os

llm = init_chat_model(model=os.getenv("OPENAI_MODEL"), model_provider="openai")

google_client = genai.Client(api_key=os.getenv("X_GOOGLE_API_KEY"))


