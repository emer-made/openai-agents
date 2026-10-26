from dotenv import load_dotenv
from agents import Agent, Runner
from pydantic import BaseModel, Field

load_dotenv(override=True)

MODEL="gpt-5.4-mini"

INSTRUCTIONS = """
You are a senior researcher tasked with writing a cohesive report for a research query.
You will be provided with the original query, and some research.
Generate a comprehensive report based on the research and the query.
The final output should be in markdown format, and it should be lengthy and detailed. Aim 
for 5-10 pages of content, at least 1000 words.
"""

class ReportData(BaseModel):
    short_summary: str = Field(description="")
    markdown_report:str = Field(description="")
    follow_up_questions: str = Field(description="")


async def write_report(query: str, search_results: list[str]) -> ReportData:
    """ Write the report for the query """
    input_message = f"Original query: {query}\nSummarized search the results: {search_results}"
    writer_agent = Agent(name="Writer Agent", model=MODEL, instructions=INSTRUCTIONS, output_type=ReportData)
    result = await Runner.run(writer_agent, input_message)
    return result.final_output
