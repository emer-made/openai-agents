import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, output_guardrail, GuardrailFunctionOutput
from pydantic import BaseModel, Field

load_dotenv(override=True)

class EmailReview(BaseModel):
    is_professional: bool = Field(description="Whether the email is professional or not")
    sentences: int = Field(description="Number of sentences in the email.")
    contains_placeholder: bool = Field(description="Whether the email contains place holders.")


async def generate_email():
    pirate = Agent(name="Cowboy Email", model="gpt-5.4-mini", instructions="You are an assistant that generates emails.", output_guardrails=[guardrail_output])
    result = await Runner.run(pirate, "Generate an cold calling email to sell an air purifier. Talk like a cowboy and keep it short.")
    print(result.final_output)


@output_guardrail
async def guardrail_output(ctx, agent, message):
    checker = Agent(name="checker", model="gpt-5.4-mini", instructions="You are a professional email checker.", output_type=EmailReview)
    result = await Runner.run(checker, message, context=ctx)
    review = result.final_output
    has_problem = review.contains_placeholder or (not review.is_professional)
    return GuardrailFunctionOutput(output_info={"review": review}, tripwire_triggered=has_problem)


if __name__ == "__main__":
    # Output guardrails.
    asyncio.run(generate_email())