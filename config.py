import os

ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"

DEFAULT_MODEL = "chatgpt"

MODEL_CONFIG = {
    "chatgpt": {
        "cost": 0.0002,
        "speed": "medium",
        "quality": "high"
    },
    "gemini": {
        "cost": 0.0005,
        "speed": "fast",
        "quality": "high"
    },
    "hugging-ai": {
        "cost": 0.0001,
        "speed": "fast",
        "quality": "medium"
    }
}

def get_model_config(model_name: str):
    return MODEL_CONFIG.get(model_name)
