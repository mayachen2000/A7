# Product Requirements Document (PRD)

## 1. Purpose
The purpose of this project is to build a local desktop GUI chat application in Python that integrates with a local Ollama API instance. This is a bonus assignment for an LLM (Large Language Model) course, designed to demonstrate local AI model interaction, clean software engineering workflows, and user interface design without relying on paid external cloud APIs.

## 2. Target Users
- **Course Instructors/Evaluators**: Reviewing the assignment for technical correctness, clean code structure, and professional UI.
- **Developers / Users**: Looking to chat with a lightweight, local, privacy-respecting LLM right from their desktop.

## 3. Assignment Requirements
- **Local Runtime**: The application must run entirely locally, utilizing a local instance of Ollama.
- **Custom GUI**: A desktop interface built in Python.
- **Ollama Integration**: Communicating with Ollama's chat completion endpoint (`http://localhost:11434/api/chat`).
- **Clean Structure**: Separation of concerns between the API client logic and the GUI logic.
- **Verification & Testing**: A clear way to verify the API connection (e.g., via a smoke test) and confirm correct operation.

## 4. Functional Requirements
- **Chat Interface**: Users can input text prompts and receive replies from the local model.
- **Conversation History**: The app must maintain the ongoing chat history in-memory and send the full context with each request, allowing for a natural back-and-forth conversation.
- **Clear/Reset Conversation**: A button or menu option to clear the conversation log and reset the in-memory context.
- **API Custom Headers**: Inclusion of a custom practice header `X-API-Key` in requests to simulate professional API practices.
- **Connection Diagnostics**: Automatic checks to detect if Ollama is offline or if a connection timeout occurs, reporting friendly errors to the user instead of crashing.
- **Model Configuration**: Configuration parameters (endpoint, model, timeout, API key) must be externalized using environment variables (`.env` file) or fall back to safe defaults.

## 5. Non-Functional Requirements
- **Performance**: High responsiveness. Message sending and UI updating should happen asynchronously (e.g., in a separate thread) to prevent the GUI window from freezing during API requests.
- **Privacy & Local Security**: No real external API keys or user data must be sent across the internet. Everything is processed locally on `localhost`.
- **Maintainability & Code Quality**: Follow standard Python conventions (PEP 8), with descriptive variable names, clear docstrings, and clean modularity.
- **No Paid Cloud Dependence**: Explicitly design the application to avoid any paid cloud services, reducing operational cost to zero.

## 6. GUI Requirements
- **Framework**: `CustomTkinter` for a sleek, modern, platform-native look and dark/light theme support.
- **Layout**:
  - **Header**: Application title and clear status indicator showing if the client is connected or ready.
  - **Chat Area**: Scrollable text/textbox area showing user prompts and assistant responses using distinct formatting (e.g., distinct background bubbles, alignments, or labels).
  - **Input Area**: Text entry field spanning the width of the window, allowing multi-line inputs if needed.
  - **Actions**: A "Send" button to dispatch messages, and a "Clear Chat" button to reset the conversation.
- **UX & Accessibility**:
  - Bind the `Enter` or `Ctrl+Enter` key to send messages.
  - Show a loading/thinking indicator (e.g., "Ollama is typing...") when waiting for a response.
  - Smooth window resizing with a set minimum size to prevent the interface from collapsing.

## 7. Ollama API Requirements
- **Endpoint**: `http://localhost:11434/api/chat`
- **Payload Schema**:
  - `model`: A string specifying the pulled model (default `smollm:135m`).
  - `messages`: A list of message objects, where each object has:
    - `role`: `"user"` or `"assistant"`.
    - `content`: The text content of the message.
  - `stream`: `false` (standard non-streaming JSON responses for easy, reliable parsing).
- **Custom Headers**: Must include `"Content-Type": "application/json"` and `"X-API-Key"` (populated from environment config).

## 8. Security & Secrets Handling
- **No Hardcoded Credentials**: Real or mock API keys must not be hardcoded in Python files.
- **Environment Separation**: Leverage `.env` files for configuration. Add `.env` to `.gitignore` so local development values are never checked into git.
- **No Real Paid Keys**: Use a mock local key (`local-dev-key`) to satisfy the header requirement without exposing actual paid provider secrets.

## 9. Success Criteria
1. The application starts without errors or warnings.
2. The user can successfully chat with the local model, seeing consecutive questions and answers.
3. Connection failure (Ollama service stopped) is handled gracefully with an in-app error banner or modal.
4. "Clear Chat" effectively resets both the GUI view and the underlying memory structure.
5. Code passes smoke testing, executes without crashes, and satisfies all guidelines of the bonus assignment.
