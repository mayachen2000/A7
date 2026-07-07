# Development & Implementation Plan (PLAN)

## 1. Architecture
The application is structured around a decoupled, modular design separating the User Interface (UI), Business/API Logic, and System Configuration. This guarantees that each component is individually testable and maintainable.

```
┌─────────────────────────────────────────────────────────┐
│                       GUI Layer                         │
│                    (src/gui.py)                         │
└───────────┬─────────────────────────▲───────────────────┘
            │ 1. Triggers chat        │ 4. Updates log
            │    on Background Thread │    with response
┌───────────▼─────────────────────────┴───────────────────┐
│                    Ollama Client Service                │
│                 (src/ollama_client.py)                  │
└───────────┬─────────────────────────────────────────────┘
            │ 2. Dispatches local HTTP POST
            │    with message history & X-API-Key
┌───────────▼─────────────────────────────────────────────┐
│                 Local Ollama API Daemon                 │
│               (http://localhost:11434)                  │
└─────────────────────────────────────────────────────────┘
```

### Components
- **Configuration Module (`src/config.py`)**: Loads environment variables using `python-dotenv` and defines global defaults. It acts as the single source of truth for variables such as Ollama endpoints, model selection, timeouts, and custom simulated headers.
- **Ollama Client Service (`src/ollama_client.py`)**: A wrapper around Python's `requests` library. It maintains zero UI references, allowing it to be easily smoke-tested in isolation. It handles compiling the message history list, formatting JSON payloads, inserting custom simulated API key headers, and converting raw exception types into descriptive exceptions (`OllamaError`).
- **GUI View & Threading Model (`src/gui.py`)**: Built on top of **DearPyGui (DPG)**. It renders visual components, tracks user-facing state, and captures user input. To keep the GUI smooth and prevent the window from freezing during HTTP requests, message dispatching is delegated to a separate background worker thread using Python's `threading` library, which safely schedules visual updates back onto the main event loop via a thread-safe `queue.Queue` processor.

---

## 2. Technology Stack
- **Language**: Python 3 (standard version installed in the local `.venv`).
- **UI Framework**: `DearPyGui` (Modern, fast, hardware-accelerated desktop canvas, chosen to resolve macOS-specific Tkinter rendering/startup issues).
- **HTTP Client**: `requests` (Simplicity, reliability, and robust timeout handling).
- **Environment Management**: `python-dotenv` (Safe extraction of variables from a local `.env` file).
- **Local Model Host**: `Ollama` running as a background daemon.
- **Target Model**: `smollm:135m` (A highly optimized, lightweight model to limit local compute consumption and keep testing fast and responsive).

---

## 3. Directory & File Structure
```
/
├── .env.example                # Template for configuring local environmental overrides
├── .gitignore                  # Prevents committing of local virtual environment and .env secrets
├── main.py                     # Primary entrypoint for launching the GUI application
├── PRD.md                      # Product Requirements Document (Core rules and constraints)
├── PLAN.md                     # This development and architecture plan
├── TODO.md                     # Live task checklist tracking progress
├── PROMPT_LOG.md               # Log of instructions and prompts utilized during development
├── TOKEN_COST_AWARENESS.md     # Strategy for zero-cost and lightweight local execution
├── TESTING.md                  # Test specifications and status of verification checks
├── requirements.txt            # Python package dependencies
├── docs/
│   ├── API_DOCUMENTATION.md    # API schema and payload documentation
│   └── QA_REPORT.md            # Quality assurance validation and verification logs
├── screenshots/
│   └── app_running.png         # Screenshot evidence of successful manual GUI chat interaction
├── scripts/
│   ├── api_smoke_test.py       # Standalone CLI validation script for Ollama connection
│   └── run_app.sh              # Quickstart launcher shell script
└── src/
    ├── __init__.py             # Exposes directory as a Python package
    ├── config.py               # Environmental configuration loader
    ├── gui.py                  # DearPyGui-based responsive interface and threading queue
    └── ollama_client.py        # Isolated API interaction layer
```

---

## 4. Development Phases
1. **Phase 1: Environment & Daemon Initialization** (Completed)
   - Establish local directory, initialize git, and set up `.venv`.
   - Install dependencies (`requests`, `python-dotenv`, and eventually `dearpygui`).
   - Download and start Ollama, pulling the `smollm:135m` model.
2. **Phase 2: Service Layer & Smoke Testing** (Completed)
   - Design and implement `src/config.py`.
   - Develop `src/ollama_client.py` incorporating robust request schemas and customized headers.
   - Run `scripts/api_smoke_test.py` to confirm the local setup is fully functional.
3. **Phase 3: GUI Development & Integration** (Completed)
   - Drafted initial CustomTkinter layout, which encountered local macOS rendering crashes and unresponsive blank states.
   - Re-architected visual layer to **DearPyGui**, spawning a stable, dark-themed hardware-accelerated desktop viewport.
   - Developed thread-safe communication between GUI elements and the client service using an internal response queue.
   - Maintained conversation context in-memory.
4. **Phase 4: Bug Resolution, Testing & Verification** (Completed)
   - Resolved the window initialization block entirely by migrating from Tcl/Tk system packages to DPG's custom drawing engine.
   - Integrated user input validations (to block empty prompts) and friendly status/error labels in code.
   - Conducted manual end-to-end chat validation, verifying responsive rendering.
   - Saved visual verification artifact to `screenshots/app_running.png`.
5. **Phase 5: Documentation & Submission Preparation** (Completed)
   - Completed `README.md`, `API_DOCUMENTATION.md`, `QA_REPORT.md`, `TODO.md`, `TESTING.md`, and `TOKEN_COST_AWARENESS.md` to ensure absolute alignment, clarity, and grading readiness.

---

## 5. Testing Plan
- **Automated Client Validation**: Run `api_smoke_test.py` to ensure local API availability, correct model loading, and non-empty responses.
- **Manual GUI Execution**: Verify main loop initialization, layout rendering, visual responsiveness under load, and proper element centering on macOS.
- **Functional Flow Validation**:
  - Send message -> receive response -> verify chat history in UI.
  - Send second message -> verify response is populated.
  - Click "Clear Chat" -> verify visual conversation log and client memory are cleared.
- **Robust Exception/Edge Case Validation**:
  - *Ollama offline*: Shut down the Ollama service, send a message, and verify that the GUI displays a friendly error inside the log instead of crashing or hanging.
  - *Empty input*: Verify that clicking send or pressing enter on an empty message does not dispatch an API request and updates status.
  - *Timeout testing*: Emulate a high timeout threshold to verify background threading works seamlessly and does not block the UI.

---

## 6. Documentation Plan
- Maintain updated markdown documents in the root directory to guide development.
- Write a clear, comprehensive `docs/API_DOCUMENTATION.md` outlining the payload structures and expected JSON formatting.
- Construct `docs/QA_REPORT.md` following testing to log actual execution outcomes.
- Write a clean `README.md` to facilitate zero-effort setup and reproduction.

---

## 7. GitHub & Version Management Plan
- Keep configurations completely isolated from commits. Use `.gitignore` to prevent any local virtual environment folders or `.env` files from leaking.
- Perform a thorough audit of modified files prior to finalizing the repository stage.

---

## 8. Current Implementation Status
- **Successes**:
  - Git repository structure is established.
  - Python virtual environment is set up and activated.
  - `requirements.txt` dependencies are fully installed.
  - Ollama local service is up and running, with `smollm:135m` model loaded.
  - Isolated API communication is verified: `scripts/api_smoke_test.py` successfully sends "Hello" and receives a response from local Ollama.
  - GUI startup crashes and macOS blank-rendering issues have been fully resolved by transitioning to a high-performance **DearPyGui** visual layer.
  - Thread-safe background execution is implemented and supported successful manual GUI interaction.
  - Visual proof preserved at `screenshots/app_running.png`.
  - Project, API, and QA documentation has been updated and is ready for final Git audit, commit, push, and repository verification.
