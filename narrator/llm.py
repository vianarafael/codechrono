import requests

MODEL_NAME = "qwen3:14b-q4_K_M" # Change to the model you are using

def run_llm(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
    )
    return response.json().get("response", "").strip()