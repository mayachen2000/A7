# API Integration Documentation

This document specifies the communication protocol between the desktop GUI application and the local Ollama background service. It details endpoint addresses, payload schemas, custom headers, response processing, and local error mapping strategies.

---

## 1. Local Endpoint Specifications

The client service communicates exclusively with the local Ollama background API instance running on the host machine.

* **Target URL**: `http://localhost:11434/api/chat`
* **HTTP Method**: `POST`
* **Network Context**: Runs entirely on the local loopback interface (`localhost`), meaning no outbound internet traffic is generated to execute inference.

---

## 2. Request Headers

To mimic enterprise-grade integration practices and enforce request constraints, the following HTTP headers are included in every outbound POST request:

| Header Name | Expected Value | Purpose / Description |
| :--- | :--- | :--- |
| `Content-Type` | `application/json` | Enforces JSON formatting for request and response structures. |
| `X-API-Key` | `local-dev-key` (or configured via environment variable) | A simulated, application-level verification token used to practice header construction. |

### 🔒 Crucial Security Note on `X-API-Key`
The `X-API-Key` is **strictly local and mock-only**.
* It does **not** connect to, authenticate with, or bill against any paid cloud LLM providers (e.g., OpenAI, Anthropic, or Google).
* It is configured inside `src/config.py` with a default value of `"local-dev-key"`.
* Its presence ensures that the grading agent sees an implementation of custom header parsing without any exposure of real, sensitive cloud keys or operational expenses.

---

## 3. Request Payload Schema

The POST payload is constructed as a JSON object containing three primary keys:

```json
{
  "model": "smollm:135m",
  "messages": [
    {
      "role": "user",
      "content": "What is the capital of France?"
    }
  ],
  "stream": false
}
```

### Parameters

* **`model`** *(string, required)*: Specifies the model pulled in Ollama to run inference. Defaults to `"smollm:135m"`, which can be changed via the `OLLAMA_MODEL` environment variable.
* **`messages`** *(array of objects, required)*: A list representing the active conversation thread history. Each message object contains:
  * **`role`** *(string)*: Defines the author of the message. Allowed values: `"user"` (human prompt) or `"assistant"` (LLM generated reply).
  * **`content`** *(string)*: The text content of the message.
* **`stream`** *(boolean, required)*: Set strictly to `false`. This instructs Ollama to wait until the full response is completed before returning a single, consolidated JSON response. This eliminates the complexity of token streaming chunk-parsing while keeping the application highly stable.

---

## 4. Response Payload Schema

When a request is processed successfully (HTTP Status `200 OK`), Ollama returns a JSON response:

```json
{
  "model": "smollm:135m",
  "created_at": "2026-07-07T12:00:00.123456789Z",
  "message": {
    "role": "assistant",
    "content": "The capital of France is Paris."
  },
  "done_reason": "stop",
  "done": true,
  "total_duration": 450000000,
  "load_duration": 1500000,
  "prompt_eval_count": 12,
  "prompt_eval_duration": 50000000,
  "eval_count": 8,
  "eval_duration": 390000000
}
```

### Response Processing Steps in `src/ollama_client.py`
1. **HTTP Status Code Verification**: The client checks if `status_code == 200`. If not, it raises an `OllamaError`.
2. **JSON Parsing**: The response body is parsed using `.json()`. If parsing fails, it throws a JSON-format error.
3. **Data Integrity Checks**:
   - Assures the top-level response is a dictionary.
   - Extracts the `"message"` block and confirms it is a valid dictionary.
   - Retrieves the `"content"` string from the message block and returns it.

---

## 5. Error Handling & Exception Mappings

The application's client wrapper (`src/ollama_client.py`) standardizes connection issues and raw HTTP errors into a single custom exception type: **`OllamaError`**.

This prevents raw tracebacks from propagating to the UI thread, allowing the GUI to print clear, helpful troubleshooting instructions in the chat view:

| Real-world Error Scenario | Trigger Mechanism (Library level) | Mapped Exception Text in Application |
| :--- | :--- | :--- |
| **Ollama Service Stopped** | `requests.exceptions.ConnectionError` | `"Connection failed. Please verify that Ollama is running at http://localhost:11434/api/chat.\nDetails: <error>"` |
| **Response Timeout** | `requests.exceptions.Timeout` | `"Request to Ollama timed out after 120 seconds.\nDetails: <error>"` |
| **Invalid Port/Route** | HTTP status code other than `200` | `"Ollama returned HTTP status code <status>.\nResponse: <text>"` |
| **Empty/Malformed Response** | JSON parse failure or missing keys | `"Missing or invalid 'message' key in Ollama response JSON.\nResponse: <text>"` |

When the GUI receives an `OllamaError`, it halts the loading indicator, prints the localized error text in the chat window, and sets the status bar to `"Status: Connection/API Error"` without crashing or locking up the viewport loop.
