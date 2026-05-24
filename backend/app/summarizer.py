import requests
import os

SUMMARIZE_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
GENERATE_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

def call_hf_api(api_url, text, payload_extra=None):
    hf_api_key = os.getenv("HF_API_KEY")
    if not hf_api_key:
        return "Server error: HF_API_KEY environment variable is missing"

    headers = {
        "Authorization": f"Bearer {hf_api_key}"
    }

    # Truncate text to avoid model limits
    if len(text) > 3500:
        text = text[:3500]

    payload = {"inputs": text}
    if payload_extra:
        payload.update(payload_extra)

    try:
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code != 200:
            return f"Error: {response.json()}"

        data = response.json()

        # Handle different response formats
        if isinstance(data, list) and len(data) > 0:
            if "summary_text" in data[0]:
                return data[0]["summary_text"]
            if "generated_text" in data[0]:
                return data[0]["generated_text"]
        
        # If Hugging Face returns a dict instead of a list (happens sometimes on some models/endpoints)
        if isinstance(data, dict):
            if "summary_text" in data:
                return data["summary_text"]
            if "generated_text" in data:
                return data["generated_text"]
            if "error" in data:
                return f"Error: {data['error']}"

        return "Unexpected response from model"

    except Exception as e:
        return f"Server error: {str(e)}"

def summarize_text(text):
    # Set parameters to force a more concise, smaller summary
    return call_hf_api(SUMMARIZE_API_URL, text, payload_extra={
        "parameters": {
            "max_length": 130,
            "min_length": 30,
            "do_sample": False
        }
    })

def generate_text(prompt):
    return call_hf_api(GENERATE_API_URL, prompt, payload_extra={
        "parameters": {
            "max_length": 250,
            "min_length": 10,
            "do_sample": True,
            "temperature": 0.7
        }
    })
