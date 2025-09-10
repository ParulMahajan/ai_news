from model.llm import llm
from model.prompt.customPrompt import summary_prompt, ai_title_check, create_image_prompt
from langchain.chains import LLMChain

from request.Response import PostSummary

structured_llm = llm.with_structured_output(PostSummary)
summary_chain = summary_prompt | structured_llm
image_prompt_chain = create_image_prompt | llm
title_check_chain = ai_title_check | llm


