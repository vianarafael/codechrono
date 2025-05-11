import requests

def run_llm(prompt: str, model: str = "qwen3:14b-q4_K_M") -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    return response.json().get("response", "").strip()