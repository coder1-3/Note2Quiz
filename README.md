# 📝 Note2Quiz AI

Note2Quiz AI is a completely offline, privacy-first web application that transforms your study notes into interactive multiple-choice quizzes. Built for environments with limited internet data and hardware constraints, it runs a lightweight Large Language Model (LLM) entirely on your local machine.

## ✨ Features
* **100% Offline & Private:** Uses local AI (Ollama). No API keys, no cloud processing, and no data leaves your computer.
* **Lightweight:** Powered by `qwen2.5:0.5b`, a highly efficient 400 MB model optimized for machines with 8GB RAM or integrated graphics.
* **Interactive UI:** A multi-step workflow to upload notes, configure the quiz, and preview the results.
* **Multiple Export Formats:** Download your generated quiz as a standard Text file (`.txt`), a Markdown document (`.md`), or a fully styled Web Page (`.html`).

## 🛠️ Tech Stack
* **Backend:** Python, Flask, `requests`
* **Frontend:** HTML5, CSS3, Jinja2 Templates
* **AI Engine:** Ollama (Local LLM Server)
* **Model:** Qwen 2.5 (0.5 Billion parameters)

## 📂 Project Structure
```text
note2quiz/
│
├── app.py                  # Main Flask application and AI logic
├── static/                 
│   └── style.css           # UI styling and layout
├── templates/              
│   ├── index.html          # Upload page
│   ├── configure.html      # Quiz settings (length, format)
│   └── result.html         # Preview and download page
└── temp_quizzes/           # Auto-generated folder for temporary downloads