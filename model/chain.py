from model.llm import llm
from model.prompt.customPrompt import summary_template, ai_title_check
from langchain.chains import LLMChain

summary_chain = summary_template | llm

title_check_chain = ai_title_check | llm


