VOICE_COMMANDS = {
    "clear screen": "clear",
    "run code": "run",
    "exit assistant": "exit",
    "clear": "clear",
    "run": "run",
    "exit": "exit",
}


def parse_command(text: str):
    """Identify a supported voice command from transcribed text."""
    if not text:
        return None

    normalized = text.strip().lower()
    for command, action in VOICE_COMMANDS.items():
        if command in normalized:
            return action

    return None
