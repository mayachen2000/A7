# Token & Cost Awareness Strategy (TOKEN_COST_AWARENESS)

A professional AI/LLM development approach requires careful tracking and optimization of compute costs, API expenditures, and context size overheads. This document explains the economic, architectural, and resource strategies applied to this project.

---

## 1. Zero-Cost Local Runtime Architecture

* **Local Inference via Ollama**: The final desktop chat application is engineered to communicate entirely with a locally running Ollama instance (`http://localhost:11434/api/chat`).
* **No Paid Cloud API Calls**: Because chat responses are processed and generated entirely on the user's local machine, there are zero active subscription requirements, pay-per-token charges, or third-party usage costs.
* **Economic Advantage**: This design permits unlimited testing, chat iterations, and evaluation without incurring financial liabilities or running out of trial credits.

---

## 2. Role of the Development Assistant vs. Runtime Model

* **Gemini CLI (Development Assistant)**: Gemini CLI is used exclusively as a peer programmer to help research, plan, write, and document the application code during development.
* **Runtime Separation**: Gemini CLI is **not** embedded in or accessed by the chat application during runtime. The submitted desktop application is completely independent and operates locally without accessing cloud LLM assistants.
* **Token Stewardship**: During development, we minimize context usage and prevent unnecessary prompt repetitions to use the development assistant efficiently, but once the application is delivered, its runtime cost to the student and evaluator is strictly zero.

---

## 3. Local Model Selection Strategy (`smollm:135m`)

* **Lightweight Profile**: The default model configured for this project is `smollm:135m` (approx. 135 million parameters).
* **Compute & Memory Optimization**: Selecting a small model drastically lowers the local hardware barrier:
  - Consumes less than 500MB of RAM/VRAM.
  - Generates responses in milliseconds, even on standard CPU laptops without high-end GPUs.
  - Drastically speeds up test cycles (sending a message and getting a reply is almost instantaneous).
* **Scalability**: The modular code structure allows advanced users to seamlessly switch to larger models (e.g., `llama3`, `mistral`, `gemma`) in their `.env` files if their local hardware supports it, without changing a single line of application source code.

---

## 4. Context Window & Memory Management

* **In-Memory Chat History**: The application avoids carrying unnecessary, endless system context. It maintains a clean list of dictionaries in-memory inside the GUI (`self.messages`):
  ```python
  {"role": "user"|"assistant", "content": "..."}
  ```
* **Scope Control**: Keeping a lean context history prevents payload bloat and keeps requests sent to local Ollama simple and lightweight, avoiding local inference lags and high memory overheads.
* **Clear State Operations**: The "Clear Chat" function completely resets this history, freeing up local memory and starting with a clean context.

---

## 5. Security & Practice Header Simulation (`X-API-Key`)

* **Simulated API Header**: For professional API practice, the application's client wrapper includes an `X-API-Key` header with requests.
* **No Real Secrets Committed**: The API key utilized is a dummy local value (`local-dev-key`) specified in `src/config.py`.
* **Zero Security Risk**: No real cloud provider keys (such as OpenAI, Anthropic, or Google Gemini keys) are configured or committed. This design is intended to prevent sensitive secrets or paid API credentials from being committed; the final Git audit is performed before submission.

---

## 6. Significance for Engineering Documentation

Understanding the difference between development costs (assistant tools) and runtime/production costs (local deployment) is critical in modern software engineering. By standardizing this separation, this project demonstrates a highly reproducible, robust, and cost-effective strategy for AI application design.
