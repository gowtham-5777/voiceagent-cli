"""Simple in-memory session store for last AI response and command."""

_last_ai_response = None
_last_user_command = None


def store_last_response(text: str):
    global _last_ai_response
    _last_ai_response = text


def get_last_response():
    return _last_ai_response


def store_last_command(text: str):
    global _last_user_command
    _last_user_command = text


def get_last_command():
    return _last_user_command
