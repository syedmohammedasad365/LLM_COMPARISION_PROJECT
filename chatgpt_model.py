from openai import OpenAI
import os

def chatgpt_response(prompt: str) -> str:
    api_key = os.getenv("OPEN_API_KEY")

    if not api_key:
        return " OPENAI_API_KEY not found"

    client = OpenAI(api_key="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")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content