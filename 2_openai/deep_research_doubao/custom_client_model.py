from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ARK_API_KEY = os.getenv("ARK_API_KEY")
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

doubao_client = AsyncOpenAI(base_url=ARK_BASE_URL, api_key=ARK_API_KEY)
doubao_model = OpenAIChatCompletionsModel(
    model="doubao-1-5-pro-32k-250115", openai_client=doubao_client
)

deepseek_client = AsyncOpenAI(base_url=DEEPSEEK_BASE_URL, api_key=DEEPSEEK_API_KEY)
deepseek_model = OpenAIChatCompletionsModel(
    model="deepseek-chat", openai_client=deepseek_client
)
