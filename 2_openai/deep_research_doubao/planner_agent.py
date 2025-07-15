import json
from pydantic import BaseModel, Field
from custom_client_model import doubao_model, deepseek_model
from agents import Agent, Runner, function_tool
import asyncio


class WebSearchItem(BaseModel):
    reason: str = Field(description="Reason for this search.")
    query: str = Field(description="Search term.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="List of searches.")


HOW_MANY_SEARCHES = 3

INSTRUCTIONS = f"""
You are a helpful research assistant. Given a query, come up with a set of web searches to perform to best answer the query.
Output {HOW_MANY_SEARCHES} search terms in the following JSON format:

{{
    "searches": [
        {{
            "reason": "Your reasoning for why this search is important to the query.",
            "query": "The search term to use for the web search."
        }},
        {{
            "reason": "Your reasoning for why this search is important to the query.",
            "query": "The search term to use for the web search."
        }},
        ...
    ]
}}

Strictly adhere to the following output rules:
1. Output only the JSON object - do not include any other content
2. Do not add any explanations, comments, or extra text
3. Do not use Markdown code block markers
4. Ensure 100% correct JSON formatting
"""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    # model=doubao_model,
    model=deepseek_model,
    output_type=WebSearchPlan,
)

async def main():
    # This agent will use the custom LLM provider
    result = await Runner.run(planner_agent, "AI Agent 发展趋势")
    try:
        # 手动解析JSON
        data = json.loads(result.final_output)
        plan = WebSearchPlan(**data)
        print("解析成功:")
        for i, search in enumerate(plan.searches, 1):
            print(f"{i}. 原因: {search.reason}")
            print(f"   搜索: {search.query}")
    except Exception as e:
        print(f"JSON解析失败: {e}")
        print("原始输出内容:")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
