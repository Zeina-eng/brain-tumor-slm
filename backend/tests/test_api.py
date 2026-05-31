import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Add current dir so it can find app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from app.main import app
    client = TestClient(app)
except Exception as e:
    print(f"Error importing app: {e}")
    sys.exit(1)

class TestAPI(unittest.TestCase):
    @patch("app.summarizer.requests.post")
    def test_summarize_text_input(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"summary_text": "Mock summary"}]
        mock_post.return_value = mock_response

        # Need to set env var for the token
        os.environ["HF_API_KEY"] = "fake_token"

        response = client.post("/summarize", data={"text": "This is a test document to summarize."})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"summary": "Mock summary"})

    @patch("app.summarizer.requests.post")
    def test_summarize_missing_input(self, mock_post):
        response = client.post("/summarize")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Either 'text' or 'file' must be provided.", response.json()["detail"])

    @patch("app.summarizer.requests.post")
    def test_summarize_txt_upload(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"summary_text": "File summary mock"}]
        mock_post.return_value = mock_response

        os.environ["HF_API_KEY"] = "fake_token"

        files = {'file': ('test.txt', b'This is some txt content.', 'text/plain')}
        response = client.post("/summarize", files=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"summary": "File summary mock"})

    # Let's verify HF error handling too
    @patch("app.summarizer.requests.post")
    def test_hf_api_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid token"}
        mock_post.return_value = mock_response

        os.environ["HF_API_KEY"] = "fake_token"

        response = client.post("/summarize", data={"text": "Text to fail."})
        self.assertEqual(response.status_code, 401)
        self.assertIn("Hugging Face API Error: Invalid token", response.json()["detail"])

if __name__ == "__main__":
    unittest.main()
