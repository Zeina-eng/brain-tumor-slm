import requests
import os

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

def summarize_text(text):
    hf_api_key = os.getenv("HF_API_KEY")
    if not hf_api_key:
        return "Server error: HF_API_KEY environment variable is missing"

    headers = {
        "Authorization": f"Bearer {hf_api_key}"
    }

    # Truncate text to avoid 'index out of range' (BART maxes out at 1024 tokens)
    # 3500 chars is a safe estimate for 1024 tokens.
    if len(text) > 3500:
        text = text[:3500]

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})

        if response.status_code != 200:
            return f"Error: {response.json()}"

        data = response.json()

        if isinstance(data, list) and "summary_text" in data[0]:
            return data[0]["summary_text"]

        return "Unexpected response from model"

    except Exception as e:
        return f"Server error: {str(e)}"