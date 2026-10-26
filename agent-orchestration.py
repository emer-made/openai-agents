import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv(override=True)


# Orchestration by code.
async def orchestrate_code(message):
    monday_doctor = Agent(name="Doctor Monday", model="gpt-5.4-mini", instructions="You are a doctor who treats only adults. Respond with 'Available' only for Monday appointment otherwise say 'Not Available'. Do not explain your answer.")
    tuesday_doctor = Agent(name="Dr. Tuesday", model="gpt-5.4-mini", instructions="You are a doctor who treats only adults. Respond with 'Available' only for Monday appointment otherwise say 'Not Available'. Do not explain your answer.")
    all_week_doctor = Agent(name="Dr. Kiddo", model="gpt-5.4-mini", instructions="You are a doctor who treats only children. Reject appointments that are not for kids. Respond with 'Available' only for weekday appointments otherwise say 'Not Available'. Do not explain your answer.")

    results = await asyncio.gather(
        Runner.run(monday_doctor, message),
        Runner.run(tuesday_doctor, message),                                              
        Runner.run(all_week_doctor, message)
    )
    doctor = [
                result.last_agent.name 
                for result in results
                if result.final_output.lower().strip().rstrip() == "available"
             ]
    reply = "Your appointment is with " + doctor[0] if doctor else "Sorry, we don't have an available doctor."
    print(reply)


# Orchestration by tools.
async def orchestrate_tools(message):
    spanish = Agent(name="Spanish Translator", model="gpt-5.4-mini", instructions="You are an assistant that translate English to Spanish")
    french = Agent(name="French Translator", model="gpt-5.4-mini", instructions="You are an assistant that translate English to Frech")
    italian = Agent(name="Italian Translator", model="gpt-5.4-mini", instructions="You are an assistant that translate English to Italian")

    spanish_tool = spanish.as_tool(tool_name="spanish_tool", tool_description="Use this tool to translate from English to Spanish")
    french_tool = french.as_tool(tool_name="french_tool", tool_description="Use this tool to translate English to French")
    italian_tool = italian.as_tool(tool_name="italian_tool", tool_description="Use this tool to translate English to Italian")
    tools = [spanish_tool, french_tool, italian_tool]
    agent = Agent(name="Translator", model="gpt-5.4-mini", instructions="You are an assistant that routes translation requests to appropriate translators.", tools=tools)
    result = await Runner.run(agent, message)
    print(result.final_output)


# Orchestration by handoffs.
async def orchestrate_handoffs(message):
    spanish = Agent(name="Spanish Translator", model="gpt-5.4-mini", instructions="You are an assistant that translate English to Spanish")
    french = Agent(name="French Translator", model="gpt-5.4-mini", instructions="You are an assistant that translate English to Frech")
    italian = Agent(name="Italian Translator", model="gpt-5.4-mini", instructions="You are an assistant that translate English to Italian")

    handoffs = [spanish, french, italian]
    agent = Agent(name="Translator", model="gpt-5.4-mini", instructions="You are an assistant that routes translation requests to appropriate translators.", handoffs=handoffs)
    result = await Runner.run(agent, message)
    print(result.final_output)


if __name__ == "__main__":
    # code orchestration
    # appointment = "I want to see a doctor on Friday for my kid."
    # asyncio.run(orchestrate_code(appointment))

    # tools orchestration
    # message = """
    # Translate this English to Italian:

    # 'The sky looks gray because of haze from the wild fires.
    # Use tool available to you.
    # """
    # asyncio.run(orchestrate_tools(message))

    # tools orchestration
    message = """
    Translate this English to French:

    'It is a rainy day today.
    Pass to the appropriate translator to get your answer. Do not do the translation yourself.
    """
    asyncio.run(orchestrate_tools(message))