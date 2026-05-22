import os
import re

from dotenv import load_dotenv
from interpreter import interpreter
from agent.interpreter_wrapper import send_to_llm
from utils.helpers import print_error, print_info


# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()


# =========================
# CONFIGURATION
# =========================

API_BASE = "https://api.groq.com/openai/v1"
MODEL_NAME = "groq/llama-3.3-70b-versatile"
GROQ_KEY_ENV = "GROQ_API_KEY"


# =========================
# GLOBAL INTERPRETER CONFIG
# =========================

interpreter.auto_run = True
interpreter.offline = False


# =========================
# HELPERS
# =========================

def _sanitize_terminal_output(text: str) -> str:
    """Remove ANSI escape sequences and normalize whitespace."""

    if not isinstance(text, str):
        text = str(text)

    ansi_re = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    cleaned = ansi_re.sub("", text)

    return cleaned.replace("\r\n", "\n").strip()


# =========================
# MAIN FUNCTION
# =========================

def send_to_open_interpreter(prompt: str) -> str:
    """
    Send prompt to Open Interpreter using Groq backend.
    """

    if not prompt or not prompt.strip():
        return "No text was provided."

    print_info("Sending transcription to Open Interpreter (Groq)...")

    groq_api_key = os.getenv(GROQ_KEY_ENV)

    if not groq_api_key:
        error_message = (
            f"{GROQ_KEY_ENV} environment variable is not set."
        )

        print_error(error_message)

        return error_message

    try:

        # =========================
        # REQUIRED ENV VARIABLES
        # =========================

        os.environ["OPENAI_API_KEY"] = groq_api_key
        os.environ["OPENAI_API_BASE"] = API_BASE

        # =========================
        # INTERPRETER CONFIG
        # =========================

        interpreter.llm.api_key = groq_api_key
        interpreter.llm.api_base = API_BASE
        interpreter.llm.model = MODEL_NAME

        # =========================
        # SEND PROMPT
        # =========================
        interpreter.model = MODEL_NAME
        response = interpreter.chat(prompt)

        # =========================
        # HANDLE RESPONSE
        # =========================

        if isinstance(response, str):
            result = response

        elif isinstance(response, list):

            result = "\n".join(
                [
                    str(item.get("content", ""))
                    for item in response
                    if isinstance(item, dict)
                ]
            )

        else:
            result = str(response)

        cleaned_response = _sanitize_terminal_output(result)

        return cleaned_response or "Open Interpreter returned an empty response."

    except Exception as exc:

        print_error(f"Open Interpreter failed: {exc}")

        return f"Unable to contact Open Interpreter: {exc}"