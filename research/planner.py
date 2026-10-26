from dotenv import load_dotenv
from agents import Agent, Runner
from pydantic import BaseModel, Field

load_dotenv(override=True)

MODEL="gpt-5.4-mini"

NUMBER_OF_SEARCHES=5

INSTRUCTION=f"""
You are a research assistant. Given a user query, generate a set of web searches
to perform to answer the query. Output {NUMBER_OF_SEARCHES} search queries to perform. 
"""


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")
    

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list term to search in the web to best answer the query.")


async def plan_search(query: str) -> WebSearchPlan:
    """Plan the searches that will be performed to answer the query."""
    planner_agent = Agent("Planning Agent", model=MODEL, instructions=INSTRUCTION, output_type=WebSearchPlan)
    result = await Runner.run(planner_agent, f"Query: {query}")
    return result.final_output
