# AI Study Companion

A full-stack AI-powered web application that transforms uploaded PDF documents into structured study materials using the Anthropic Claude API.

## What it does

Upload any lecture notes or academic PDF and the app will automatically generate:

- **Summaries** — key concepts broken down into clear bullet points grouped by topic
- **Flashcards** — question and answer pairs for active recall practice
- **Quizzes** — multiple choice questions with explanations for incorrect answers

## How it works

1. Upload a PDF through the web interface
2. The document is parsed and chunked into segments that fit within the LLM context window
3. Each chunk is sent to the Claude API with structured prompts that return JSON
4. The JSON is parsed and rendered as interactive study content

## Tech Stack

- **Python** — core application logic
- **Anthropic Claude API** — language model for content generation
- **Streamlit** — web interface and UI components
- **PyPDF2** — PDF parsing and text extraction

## Running locally

```bash
git clone https://github.com/Juuexe/AI-Study-Companion
cd AI-Study-Companion
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add your API key to a `.env` file:

Then run:

```bash
streamlit run app.py
```

## Live Demo

[https://huggingface.co/spaces/Juuie/ai-study-companion](https://huggingface.co/spaces/Juuie/ai-study-companion)
