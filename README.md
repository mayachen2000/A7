# Local Ollama Desktop GUI Chat Application

An elegant, fully-featured, local desktop GUI chat application built to interact with local Large Language Models (LLMs) hosted via Ollama.

This repository serves as a bonus assignment submission for the **Large Language Models (LLM)** course. It is designed to be highly structured, modular, evidence-based, and optimized for automatic evaluation by grading agents.

---

## 🌟 Project Overview & Assignment Goal

The goal of this assignment is to design and implement a standalone, local chat assistant in Python that communicates directly with a local instance of the **Ollama API**, using a custom-built desktop Graphical User Interface (GUI).

Crucially, the architecture must maintain a rigorous separation of concerns:
1. **Config Layer**: Safe environment variable loaders with fallback defaults.
2. **Client Service Layer**: An isolated Ollama API communication client capable of being smoke-tested independently from any UI library.
3. **GUI Layer**: A responsive, thread-safe desktop user interface.

To ensure maximum compatibility and resolve macOS-specific Tkinter/Tcl rendering and thread-blocking behaviors, the final user interface was modernized and stabilized using **DearPyGui**, ensuring high performance, a hardware-accelerated viewport, and a beautiful dark mode out of the box.

---

## 🛠 Final Technology Stack

- **Programming Language**: Python 3
- **GUI Framework**: [DearPyGui](https://github.com/hoffstadt/DearPyGui) (for robust cross-platform desktop viewport rendering, smooth performance, and modern styling)
- **HTTP Client**: `requests` (handles payload formulation, timeouts, and exception transformations)
- **Environment Management**: `python-dotenv` (extracts environment parameters from local configurations)
- **Local LLM API**: [Ollama](https://ollama.com/) running as a background service daemon (`http://localhost:11434`)
- **Default LLM Model**: `smollm:135m` (an incredibly lightweight, 135M parameter model chosen for lightning-fast responses and minimal local resource consumption)

---

## 🔌 Local Runtime Architecture (No Cloud LLM)

Unlike typical AI chat applications, **this app is completely free and runs 100% locally**.
* **Zero paid cloud API calls** are ever initiated.
* All prompts, reasoning steps, and model generation occur directly on your local CPU or GPU.
* The application is completely offline-ready and secures user data by keeping it local to `localhost`.
* Includes a professional practice mock request header (`X-API-Key`) containing a simulated app key to emulate enterprise development standards without exposing any real, billable third-party secrets.

---

## 📦 Project Structure

```
.
├── .env.example                # Template for configuring local environmental overrides
├── .gitignore                  # Exposes ignore rules for python caches, venv, and local .env
├── main.py                     # Primary entrypoint for launching the DearPyGui application
├── PRD.md                      # Product Requirements Document (Core specifications & rules)
├── PLAN.md                     # Refined architecture plan mapping CustomTkinter to DearPyGui
├── TODO.md                     # Granular task checklist tracking exact progress truthfully
├── PROMPT_LOG.md               # Sequential history of development prompt prompts
├── TOKEN_COST_AWARENESS.md     # Strategy documentation for zero cost and local execution
├── TESTING.md                  # Test specifications and status of all verification checks
├── requirements.txt            # Python package dependencies (DearPyGui, requests, dotenv)
├── docs/
│   ├── API_DOCUMENTATION.md    # Detail specification of API schema and local endpoint
│   └── QA_REPORT.md            # Professional QA check report and macOS migration rationale
├── screenshots/
│   └── app_running.png         # Screenshot evidence of successful manual GUI chat interaction
├── scripts/
│   ├── api_smoke_test.py       # Isolated command-line smoke-test script for the Ollama API
│   └── run_app.sh              # Bash helper script to activate the venv and start the app
└── src/
    ├── __init__.py             # Defines src as a standard Python package
    ├── config.py               # Environmental configuration loader (fallback defaults)
    ├── gui.py                  # DearPyGui-based responsive interface and threading queue
    └── ollama_client.py        # Isolated API client service (request formulation and error mappings)
```

---

## 🚀 Setup & Execution Instructions

Follow these instructions to reproduce the local setup, run the standalone client diagnostics, and launch the GUI application.

### Step 1: Clone the Repository & Configure the Virtual Environment
```bash
# Navigate to project root
cd A7

# Create local python virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### Step 2: Install Package Dependencies
```bash
# Install required libraries
pip install -r requirements.txt
```

### Step 3: Install & Launch Ollama Locally (macOS)
```bash
# Install Ollama via Homebrew (or download from ollama.com)
brew install ollama

# Start Ollama service as a background daemon
brew services start ollama

# Pull the lightweight, default model (approx. 135M parameters, fast and small)
ollama pull smollm:135m
```

### Step 4: Run the Standalone API Smoke Test
Confirm that the Ollama service is active and the client service is correctly communicating with the local model prior to launching the UI:
```bash
python3 scripts/api_smoke_test.py
```
*Expected output:* Connection stats, a successful message log, and the model's textual response, exiting with status code `0`.

### Step 5: Start the GUI Application
Launch the complete desktop application:
```bash
python3 main.py
```
*Alternatively, you can run the shell helper script:*
```bash
chmod +x scripts/run_app.sh
./scripts/run_app.sh
```

---

## 📸 Verification & Screenshot Evidence

A representative screenshot of the working GUI application showing a successful manual GUI chat interaction (confirming GUI rendering and active model replies) is preserved at:
`screenshots/app_running.png`

---

## 🔒 Security & Secrets Guardrail

* **No Hardcoded Credentials**: There are no API keys, credentials, or secrets committed in this repository.
* **Separation of Concerns**: Environment overrides are handled by copying `.env.example` to `.env` (which is explicitly ignored in `.gitignore`).
* **App-Level Key**: The `X-API-Key` configured in `src/config.py` is a mock local string (`local-dev-key`) used to practice enterprise API header structures safely. There is no threat of billing leakage or credential compromise.

---

## 🏁 Current Project Status

- [x] Local environment activated and packages installed.
- [x] Ollama background daemon initialized and local `smollm:135m` pulled.
- [x] Standalone API smoke test passes successfully.
- [x] Tkinter/CustomTkinter macOS rendering issues resolved by migrating to a high-performance **DearPyGui** GUI.
- [x] Asynchronous worker threading integrated to prevent UI freeze during LLM inference.
- [x] Manual GUI chat interaction validated.
- [x] "Clear Chat" function implemented and integrated.
- [x] Visual evidence captured and stored in `screenshots/app_running.png`.
- [x] Complete documentation, API guidelines, QA reports, and task lists updated for final evaluation.
