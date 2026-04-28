import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def ask_llm(messages, model="gpt-4o-mini", temp=0.7, tokens=250):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temp,
        max_tokens=tokens
    )

    return response.choices[0].message.content.strip()