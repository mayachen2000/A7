import os
import sys

# Add project root to sys.path to allow imports from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ollama_client import OllamaClient, OllamaError

def main():
    """
    Sends one test message to Ollama using the project client.
    Prints endpoint, model, and success/failure status.
    Exits 0 on success, 1 on failure.
    """
    client = OllamaClient()

    print("--- Ollama API Smoke Test ---")
    print(f"Endpoint: {client.url}")
    print(f"Model:    {client.model}")
    print(f"Timeout:  {client.timeout} seconds")
    print("Sending test message: 'Hello'...")

    test_messages = [{"role": "user", "content": "Hello"}]

    try:
        response = client.chat(test_messages)
        print("\n[SUCCESS] Successfully received response from Ollama!")
        print(f"Response:\n{response}")
        sys.exit(0)
    except OllamaError as e:
        print("\n[FAILURE] Failed to communicate with Ollama local API.")
        print(f"Error Details:\n{e}")
        sys.exit(1)
    except Exception as e:
        print("\n[FAILURE] An unexpected error occurred.")
        print(f"Error Details:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
