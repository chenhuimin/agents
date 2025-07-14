from pydantic import BaseModel, Field
from custom_client_model import doubao_model, deepseek_model
from agents import Agent, function_tool


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
The search terms should be relevant to the query and formatted as JSON.
"""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    # model=doubao_model,
    model=deepseek_model,
    output_type=WebSearchPlan,
)
