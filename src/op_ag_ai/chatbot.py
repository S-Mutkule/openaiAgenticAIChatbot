import chainlit as cl
from agents import Agent, OpenAIChatCompletionsModel, Runner
from openai import OpenAI, AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

@cl.on_chat_start
async def start():
    banner = cl.CustomElement(name="PersistentBanner")
    await cl.Message(
        content="",
        elements=[banner]
    ).send()

@cl.on_window_message
async def on_window_message(message : str):
    await cl.Message(
        content="This is Agentic AI Chatbot"
    ).send()

@cl.on_message
async def main(message : cl.Message):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    print(f"the message received is {message.content}")
    print(f"the gemini api key is {gemini_api_key}")
    client = AsyncOpenAI(
        api_key=gemini_api_key, 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )
    agent : Agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant that can answer questions and help with tasks.",
        model=model
    )
    result = await Runner.run(agent, message.content)
    await cl.Message(
        content=result.final_output,
    ).send()