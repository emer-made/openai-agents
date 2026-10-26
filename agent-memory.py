from dotenv import load_dotenv
from agents import Agent, Runner, trace, SQLiteSession
import asyncio

load_dotenv(override=True)

# Receptionist will get the name first.
receptionist = Agent(name="Receptionist", model="gpt-5.4-mini", instructions="You are a jolly receptionist at a dental clinic.")
dentist = Agent(name="Dentist", model="gpt-5.4-mini", instructions="You are a dentis.")

async def process_patient(memory_mode=None):
    if memory_mode == "SQLLite":
        # Process using SQL Lite session
        session = SQLiteSession("100")
        result = await Runner.run(receptionist, "Hi. My name is John and I want to have a consultation.", session=session)
        print(result.final_output)
        result = await Runner.run(dentist, "Address the patient by his name and ask more details about the purpose of his visit.", session=session)
        print(result.final_output)
    else:
        # Process via normal to_input_list
        result = await Runner.run(receptionist, "Hi. My name is John and I want to have a consultation.")
        print(result.final_output + "\n-------------------")
        next_msg = result.to_input_list() + [{"role": "user", "content": "Address the patient by his name and ask more details about the purpose of his visit."}]
        result = await Runner.run(dentist, next_msg)
        print(result.final_output)


asyncio.run(process_patient())