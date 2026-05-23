"""Simple in-memory session store for last AI response."""

_last_ai_response = None


def store_last_response(text: str):
    global _last_ai_response
    _last_ai_response = text


def get_last_response():
    return _last_ai_response
