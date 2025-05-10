import requests
import re

NAME = "Rafael"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:14b-q4_K_M"

def build_prompt(commands, git_diff, window_log):
    prompt = "You are an AI dev assistant. Summarize the developer's coding session.\n\n"

    if commands:
        prompt += "## Commands Run:\n" + "\n".join(commands[:50]) + "\n\n"

    if git_diff:
        prompt += "## Git Changes:\n" + git_diff[:3000] + "\n\n"  # Limit size to avoid overload

    if window_log:
        prompt += "## App Usage Timeline:\n" + "\n".join(window_log[:50]) + "\n\n"

    prompt += (
        "### Summary Task:\n"
        "Summarize what was worked on: features, bugs, deployments, refactors.\n"
        "Use clear bullet points. Be concise but informative."
    )

    return prompt


def summarize_session(commands, git_diff, window_log):
    prompt = build_prompt(commands, git_diff, window_log)
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        summary = response.json()["response"]
        summary = summary = re.sub(r"<think>.*?</think>", "", summary, flags=re.DOTALL).strip()

        return summary
    except Exception as e:
        return f"⚠️ Error during summarization: {e}"
    
def estimate_time(task_description, past_sessions):
    prompt = f"You are an AI assistant that estimates how long it will take {NAME} to complete a task.\n\n"
    prompt += "Here are some of his past dev sessions:\n"

    for s in past_sessions[:10]:  # limit for now
        hours = round(s["duration"] / 3600, 2)
        prompt += f"### Session ({hours}h)\n- Feature: {s['message']}\n- Summary: {s['summary']}\n\n"

    prompt += f"Task: {task_description}\n\nHow long will this take? Respond with a time estimate and a short rationale."
    prompt += f"""
    Task: {task_description}

    Please respond with:
    1. A single estimated time range (e.g. '3–5 hours')
    2. A bullet-point breakdown (feature → time)
    3. A short note on factors that may affect the estimate
    Don't use markdown. Be concise. 
    """
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
        estimate = response.json()["response"]
        estimate = re.sub(r"<think>.*?</think>", "", estimate, flags=re.DOTALL).strip()
        return estimate
    except Exception as e:
        return f"⚠️ Error estimating time: {e}"

