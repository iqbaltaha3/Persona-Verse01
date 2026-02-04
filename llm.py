# llm.py

import json
from openai import OpenAI

client = OpenAI()
# Single reusable LLM client


def call_llm(prompt: str) -> dict:
    """
    Sends a prompt to the LLM and expects JSON back.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )

    text = response.choices[0].message.content
    # Extract model reply

    return json.loads(text)
    # Convert JSON string to Python dict
