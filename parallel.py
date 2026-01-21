from concurrent.futures import ThreadPoolExecutor
import time

from models.chatgpt_model import chatgpt_response
from models.gemini_model import gemini_response
from models.huggingface_model import hf_response
from utils.metrics import log_metrics


MODEL_FUNCTIONS = {
    "chatgpt": chatgpt_response,
    "gemini": gemini_response,
    "hugging-ai": hf_response
}


def call_model(model_name: str, prompt: str) -> str:
    start_time = time.time()

    try:
        response = MODEL_FUNCTIONS[model_name](prompt)
    except Exception as e:
        response = f"Error: {e}"

    elapsed = time.time() - start_time
    log_metrics(model_name, elapsed, len(response))

    return response


def run_parallel(prompt: str, models: list) -> dict:
    results = {}

    with ThreadPoolExecutor(max_workers=len(models)) as executor:
        futures = {
            model: executor.submit(call_model, model, prompt)
            for model in models
        }

        for model, future in futures.items():
            try:
                results[model] = future.result()
            except Exception as e:
                results[model] = f"Error: {e}"

    return results
