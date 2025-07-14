from pydantic import BaseModel, Field
from custom_client_model import doubao_client
from agents import Agent, function_tool
import json


class ReportData(BaseModel):
    short_summary: str = Field(
        description="A short 2-3 sentence summary of the findings."
    )
    markdown_report: str = Field(description="The final report in markdown.")
    follow_up_questions: list[str] = Field(
        description="Suggested topics to research further."
    )


INSTRUCTIONS = """
You are a senior researcher tasked with writing a cohesive report for a research query. 
You will be provided with the original query, and some initial research done by a research assistant.

You should first come up with an outline for the report that describes the structure and flow of the report. 
Then, generate the report and return that as your final output.

Your entire response MUST be valid JSON matching this format:
{
  "short_summary": "...",
  "markdown_report": "...",
  "follow_up_questions": ["..."]
}

Do NOT add any explanation, notes, or text outside the JSON.
The final output should be in markdown format, and it should be lengthy and detailed.
Aim for 5-10 pages of content, at least 1000 words.
"""


@function_tool
async def writer_tool(query: str, research_notes: str) -> dict:
    """Generate a structured research report in markdown format from a query and research notes."""
    response = await doubao_client.chat.completions.create(
        model="doubao-1-5-pro-32k-250115",
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {
                "role": "user",
                "content": f"Query: {query}\n\nResearch Notes: {research_notes}",
            },
        ],
    )

    text = response.choices[0].message.content
    print("\n🔍 Raw model output:\n", text)

    try:
        data = json.loads(text)
        report = ReportData(**data)
        return report.dict()
    except Exception as e:
        raise ValueError(f"❌ Failed to parse JSON. {e}")


writer_agent = Agent(
    name="WriterAgent",
    instructions="You write detailed research reports using the writer_tool.",
    tools=[writer_tool],
)
