# Project Task Checklist (TODO)

This checklist tracks the implementation and verification tasks required to finalize the bonus assignment.

## Phase 1: Environment & Platform Setup
- [x] Create project directory and initialize local Git repository
- [x] Configure standard `.gitignore` file to ignore virtual environments, cache directories, and `.env` files
- [x] Set up and activate local Python virtual environment (`.venv`)
- [x] Define dependency requirements in `requirements.txt` and install successfully
- [x] Download, install, and start Ollama service on local machine
- [x] Pull lightweight LLM model (`smollm:135m`) locally inside Ollama

## Phase 2: Client & Endpoint Verification
- [x] Implement safe application-level configurations in `src/config.py` using `dotenv`
- [x] Create isolated API client wrapper in `src/ollama_client.py` incorporating mock `X-API-Key` headers
- [x] Write standalone smoke test script `scripts/api_smoke_test.py`
- [x] Run smoke test script and receive successful responses from local Ollama endpoint

## Phase 3: GUI Development, Threading & Stabilization
- [x] Draft initial CustomTkinter application and components layout in `src/gui.py`
- [x] Discover local macOS Tkinter rendering issue and startup crashes
- [x] Re-architect and stabilize the GUI using DearPyGui (DPG) in `src/gui.py`
- [x] Implement thread-safe asynchronous queue model to prevent window freezes during inference
- [x] Build multi-turn context logic using an in-memory message history array in `src/gui.py`
- [x] Add input text validation to prevent empty prompt submissions (integrated with status warning)
- [x] Integrate error/offline fallback notifications in UI if Ollama service is unreachable

## Phase 4: Manual Validation & QA
- [x] Run manual end-to-end chat verification using the DearPyGui application (completed successfully)
- [x] Implement and integrate the "Clear Chat" behavior to reset GUI view and client history array
- [x] Capture representative screenshot of the working GUI application and store in `screenshots/` directory (saved as `screenshots/app_running.png`)

## Phase 5: Documentation & Submission Preparation
- [x] Complete `README.md` containing installation, configuration, and reproduction guides
- [x] Complete `docs/API_DOCUMENTATION.md` mapping out local request and response formats
- [x] Complete `docs/QA_REPORT.md` documenting manual testing checks and macOS transition rationale
- [x] Complete `TOKEN_COST_AWARENESS.md` explaining zero-cost runtime design and model selection
- [x] Complete `TESTING.md` documenting actual verification outputs and test status
- [x] Complete `PROMPT_LOG.md` recording development prompt history
- [x] Complete `PLAN.md` updates for architecture consistency
- [ ] Verify that no actual credentials, API keys, or temporary files are tracked by Git (pending final Git audit)
- [ ] Perform final commit of all codebase modifications (pending)
- [ ] Push local Git repository to GitHub remote (pending)
- [ ] Final GitHub verification and presentation review (pending)
- [ ] Prepare PDF/template submission if required by course (pending)
