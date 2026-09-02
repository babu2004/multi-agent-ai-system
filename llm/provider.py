import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_with_tools(messages, tools):

    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=messages,
        tools=tools,
    )

    return response