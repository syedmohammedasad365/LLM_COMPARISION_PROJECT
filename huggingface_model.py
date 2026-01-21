import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_API_KEY")
if not HF_TOKEN:
    raise RuntimeError("HF_API_KEY not found")

client = InferenceClient(token=HF_TOKEN)

def hf_response(prompt, model="mistralai/Mistral-7B-Instruct-v0.2"):
    try:
        messages = [
            {"role": "user", "content": prompt}
        ]

        response = client.chat_completion(
            model=model,
            messages=messages,
            max_tokens=256,
            temperature=0.7
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"HuggingFace error: {e}"
