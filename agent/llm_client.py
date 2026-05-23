import os
import re
from dotenv import load_dotenv
from openai import OpenAI

from utils.helpers import print_error, print_info


# Load .env
load_dotenv()


GROQ_API_KEY_ENV = os.getenv("GROQ_API_KEY")
API_BASE = os.getenv("OPENAI_API_BASE", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("GROQ_MODEL", "groq/llama-3.3-70b-versatile")


def _sanitize_terminal_output(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)

    ansi_re = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    cleaned = ansi_re.sub("", text)
    return cleaned.replace("\r\n", "\n").strip()


def _get_client():
    api_key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY_ENV
    if not api_key:
        return None, "GROQ_API_KEY is not set in environment"

    try:
        client = OpenAI(api_key=api_key, base_url=API_BASE)
        return client, None
    except Exception as exc:
        return None, str(exc)


def send_to_llm(prompt: str) -> str:
    """Send prompt to Groq-backed LLM via OpenAI-compatible client."""
    if not prompt or not prompt.strip():
        return "No text was provided."

    print_info("Sending transcription to Groq LLM...")

    client, err = _get_client()
    if err:
        print_error(err)
        return err

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a terminal coding assistant. Provide concise, code-focused responses."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        response = completion.choices[0].message.content
        cleaned = _sanitize_terminal_output(response)
        return cleaned

    except Exception as exc:
        print_error(f"Groq API error: {exc}")
        return f"Unable to contact Groq API: {exc}"
