import requests
import re
from .config import OPENROUTER_API_KEY

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"


def clean_response(text):
    # Remove markdown bold/italics
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # Remove backticks
    text = text.replace("`", "")

    return text


def ask_llm(prompt):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are an executive Business Intelligence AI assistant. Never use markdown symbols like ** or *."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 600
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        data = response.json()

        if "choices" in data:
            raw_text = data["choices"][0]["message"]["content"]
            return clean_response(raw_text)

        if "error" in data:
            return f"LLM Error: {data['error']}"

        return str(data)

    except Exception as e:
        return f"LLM Exception: {str(e)}"
