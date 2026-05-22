import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from utils.helpers import print_error, print_info


# =========================
# LOAD ENV
# =========================

load_dotenv()


# =========================
# CONFIG
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"

API_BASE = "https://api.groq.com/openai/v1"


# =========================
# CLIENT
# =========================

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url=API_BASE
)


# =========================
# HELPERS
# =========================

def _sanitize_terminal_output(text: str) -> str:

    if not isinstance(text, str):
        text = str(text)

    ansi_re = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

    cleaned = ansi_re.sub("", text)

    return cleaned.replace("\r\n", "\n").strip()


# =========================
# MAIN FUNCTION
# =========================

def send_to_open_interpreter(prompt: str) -> str:

    if not prompt or not prompt.strip():
        return "No text was provided."

    if not GROQ_API_KEY:
        return "GROQ_API_KEY not found in .env file."

    print_info("Sending transcription to Groq LLM...")

    try:

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a terminal coding assistant. "
                        "Provide concise coding-focused responses."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        response = completion.choices[0].message.content

        cleaned_response = _sanitize_terminal_output(response)

        return cleaned_response

    except Exception as exc:

        print_error(f"Groq API failed: {exc}")

        return f"Unable to contact Groq API: {exc}"
