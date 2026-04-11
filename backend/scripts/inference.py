import requests
import os

API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"

def summarize_text(text: str):
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
    }

    payload = {"inputs": text}

    response = requests.post(API_URL, headers=headers, json=payload)

    result = response.json()

    # Handle response safely
    if isinstance(result, list):
        return result[0]["summary_text"]
    else:
        return str(result)