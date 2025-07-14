from pydantic import BaseModel, Field
from custom_client_model import doubao_client
import json
from agents import Agent, function_tool


class WebSearchItem(BaseModel):
    reason: str = Field(description="Reason for this search.")
    query: str = Field(description="Search term.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="List of searches.")


HOW_MANY_SEARCHES = 3

INSTRUCTIONS = f"""
You are a helpful research assistant.
Given a user query, come up with a set of web searches to perform to best answer the query.
Output EXACTLY {HOW_MANY_SEARCHES} items.

IMPORTANT:
Your entire response MUST be valid JSON matching this format:
{{
  "searches": [
    {{
      "reason": "...",
      "query": "..."
    }},
    ...
  ]
}}
Do NOT add any explanation, notes, or text outside the JSON.
"""


@function_tool
async def planner_tool(query: str) -> dict:
    """
    Generate a web search plan for a given query.
    This tool analyzes the input and outputs a structured plan
    with multiple search terms and the reasoning behind each one.
    """
    response = await doubao_client.chat.completions.create(
        model="doubao-1-5-pro-32k-250115",
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": query},
        ],
    )

    text = response.choices[0].message.content
    print("\n🔍 Raw model output:\n", text)

    try:
        data = json.loads(text)
        plan = WebSearchPlan(**data)
        return plan.dict()
    except Exception as e:
        raise ValueError(f"❌ Failed to parse JSON. {e}")


planner_agent = Agent(
    name="PlannerAgent",
    instructions="You plan search queries using the available tools.",
    tools=[planner_tool],
)
