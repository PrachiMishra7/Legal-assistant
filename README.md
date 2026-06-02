---
title: AI Legal Assistant
emoji: ⚖️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# AI Legal Assistant

An AI-based Legal Assistant that analyzes FIR documents using IPC & CrPC provisions. It uses RAG (Retrieval-Augmented Generation) to process user queries and uploaded PDFs, matching them against legal databases.

## Live Demo
You can try the application live at the following links:
- **Main Space Page (with code & repo):** [https://huggingface.co/spaces/prachi7/ai-legal-assistant](https://huggingface.co/spaces/prachi7/ai-legal-assistant)
- **Fullscreen Web App (Direct Link):** [https://prachi7-ai-legal-assistant.hf.space](https://prachi7-ai-legal-assistant.hf.space)

## Features
- **Text Analysis:** Paste FIR text directly to identify relevant IPC & CrPC sections.
- **PDF Upload:** Upload FIR PDFs for automatic extraction and analysis.
- **RAG Engine:** Uses FAISS and sentence-transformers for fast and accurate legal section retrieval.

## Requirements
- Python 3.8+

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your_repo_url>
   cd ai-legal-assistant
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

Run the FastAPI application using Uvicorn:
```bash
uvicorn app:app --reload --port 8000
```
Then visit `http://localhost:8000` to interact with the frontend.

## Deployment

For production deployment, it is recommended to use Gunicorn with Uvicorn workers:
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
Make sure to configure your deployment environment (e.g., Render, Heroku, AWS) to install dependencies from `requirements.txt` and use the above startup command.
