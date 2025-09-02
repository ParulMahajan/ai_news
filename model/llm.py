from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from google import genai
from google.genai import types
import os



llm = init_chat_model(model="gpt-4o-mini")
llm_dalle = DallEAPIWrapper(model="dall-e-3")
google_client = genai.Client(api_key=os.getenv("X-goog-api-key"))


