# config.py
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ARK_API_KEY = os.getenv("ARK_API_KEY")
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"



