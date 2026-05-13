import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    return text.strip()

def generate_flashcards(text: str, num_cards: int = 10) -> list[dict]:
    prompt = f"""You are a study assistant. From the text below, create {num_cards} flashcards.
Return ONLY a JSON array with objects having "question" and "answer" keys. No markdown, no code fences, just raw JSON.

Text:
{text}"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(clean_json(message.content[0].text))

def generate_quiz(text: str, num_questions: int = 5) -> list[dict]:
    prompt = f"""Create {num_questions} multiple-choice questions from the text below.
Return ONLY a JSON array. Each object must have: "question", "options" (array of 4 strings), "answer" (the correct option string), "explanation".
No markdown, no code fences, just raw JSON.

Text:
{text}"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(clean_json(message.content[0].text))

def generate_summary(text: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": f"Summarize the following in clear bullet points, grouped by topic:\n\n{text}"}]
    )
    return message.content[0].text