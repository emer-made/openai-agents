from dotenv import load_dotenv
from agents import Agent, Runner, WebSearchTool, ModelSettings
from planner import WebSearchPlan, WebSearchItem
import asyncio

load_dotenv(override=True)

MODEL="gpt-5.4-mini"

INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and 
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only with the summary.
"""

settings = ModelSettings(tool_choice="required")
tools = [WebSearchTool()]


async def search(item: WebSearchItem) -> str | None:
    """ Perform the searches for one query. """
    agent = Agent("Search Agent", model=MODEL, instructions=INSTRUCTIONS, tools=tools, model_settings=settings)
    input_message = f"Search term: {item.query}\nReason for searching: {item.reason}"
    result = await Runner.run(agent, input_message)
    return result.final_output


async def process(search_plan: WebSearchPlan) -> list[str]:
    """ Perform the searches to perform for the query """
    tasks = [search(item) for item in search_plan.searches]
    return await asyncio.gather(*tasks)