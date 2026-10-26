import os
import requests
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, trace

load_dotenv(override=True)


pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"


def push(message: str):
    requests.post(
        pushover_url,
        data={
            "user": pushover_user,
            "token": pushover_token,
            "message": message
        }
    )


@function_tool
def send_joke(joke: str):
    """
    Use this tool to push or send notification.

    Args:
        joke: The joke to send as notification
    """
    # Parameters without defualt value are required while those that don't have are not.
    push(joke)


# async def tell_joke():
#     agent = Agent(name="Joker", model="gpt-5.4-mini", instructions="You are a funny AI assistant.")
#     result = await Runner.run(agent, "Tell me a joke about lawyers.")
#     return result.final_output


async def tell_joke():
    joker = Agent(name="Comedian", model="gpt-5.4-mini", tools=[send_joke])
    with trace("Sending the joke now"):
        result = await Runner.run(joker, "Send me a joke about lawyers.")
    print(result.final_output)

asyncio.run(tell_joke())
