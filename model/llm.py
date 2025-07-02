from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

llm = init_chat_model(model="gpt-4o")
llm_dalle = DallEAPIWrapper(model="dall-e-3")



