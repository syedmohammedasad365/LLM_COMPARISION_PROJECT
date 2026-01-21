from openai import OpenAI
import os

def chatgpt_response(prompt: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return "OPENAI_API_KEY not found"

    client = OpenAI(api_key="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") 

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content
