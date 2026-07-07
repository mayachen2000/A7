import requests
from src import config

class OllamaError(Exception):
    """Custom exception for Ollama API interaction errors."""
    pass

class OllamaClient:
    """
    Client for communicating with the Ollama local chat API.
    """
    def __init__(self, url=None, model=None, api_key=None, timeout=None):
        self.url = url or config.OLLAMA_URL
        self.model = model or config.OLLAMA_MODEL
        self.api_key = api_key or config.APP_API_KEY
        self.timeout = timeout if timeout is not None else config.REQUEST_TIMEOUT

    def chat(self, messages):
        """
        Sends a list of messages to the Ollama local API and returns the assistant's reply.

        Args:
            messages (list of dicts): list of message objects, e.g., [{"role": "user", "content": "Hello"}]

        Returns:
            str: The content of the assistant's response.

        Raises:
            OllamaError: If the request fails, times out, or returns invalid data/status code.
        """
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
        except requests.exceptions.ConnectionError as e:
            raise OllamaError(
                f"Connection failed. Please verify that Ollama is running at {self.url}.\nDetails: {e}"
            )
        except requests.exceptions.Timeout as e:
            raise OllamaError(
                f"Request to Ollama timed out after {self.timeout} seconds.\nDetails: {e}"
            )
        except requests.exceptions.RequestException as e:
            raise OllamaError(
                f"An error occurred while connecting to Ollama:\n{e}"
            )

        if response.status_code != 200:
            raise OllamaError(
                f"Ollama returned HTTP status code {response.status_code}.\nResponse: {response.text}"
            )

        try:
            response_json = response.json()
        except ValueError as e:
            raise OllamaError(
                f"Ollama response could not be parsed as valid JSON.\nResponse: {response.text}"
            )

        if not isinstance(response_json, dict):
            raise OllamaError(
                f"Unexpected response structure from Ollama (expected a JSON object).\nResponse: {response_json}"
            )

        message_obj = response_json.get("message")
        if not message_obj or not isinstance(message_obj, dict):
            raise OllamaError(
                f"Missing or invalid 'message' key in Ollama response JSON.\nResponse: {response_json}"
            )

        content = message_obj.get("content")
        if content is None:
            raise OllamaError(
                f"Missing 'content' key within the response message object.\nResponse: {response_json}"
            )

        return content
