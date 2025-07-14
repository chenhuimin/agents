from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from config import ARK_API_KEY, ARK_BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

doubao_client = AsyncOpenAI(base_url=ARK_BASE_URL, api_key=ARK_API_KEY)
doubao_model = OpenAIChatCompletionsModel(
    model="doubao-1-5-pro-32k-250115", openai_client=doubao_client
)

deepseek_client = AsyncOpenAI(base_url=DEEPSEEK_BASE_URL, api_key=DEEPSEEK_API_KEY)
deepseek_model = OpenAIChatCompletionsModel(
    model="deepseek-chat", openai_client=deepseek_client
)
