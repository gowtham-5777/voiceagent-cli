from interpreter import interpreter

from utils.helpers import print_error, print_info


def send_to_open_interpreter(prompt: str) -> str:
    """Send a text prompt to Open Interpreter using the Python API."""
    if not prompt.strip():
        return "No text was provided to Open Interpreter."

    print_info("Sending transcription to Open Interpreter...")

    try:
        response = interpreter.chat(prompt)

        if isinstance(response, str):
            result = response
        elif hasattr(response, "text"):
            result = response.text
        elif hasattr(response, "content"):
            result = response.content
        else:
            result = str(response)

        return result.strip() or "Open Interpreter returned an empty response."

    except Exception as exc:
        print_error(f"Open Interpreter failed: {exc}")
        return f"Unable to contact Open Interpreter: {exc}"
