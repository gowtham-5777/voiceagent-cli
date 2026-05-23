import re
from typing import Optional, Tuple


def parse_command(text: str) -> Optional[Tuple[str, Optional[str]]]:
    """Parse text and return (action, arg) or None.

    Actions: clear, help, exit, repeat, list_files, pwd, create_file, run_python, stop_listening
    """
    if not text:
        return None

    normalized = text.strip().lower()

    # Exact matches
    if normalized in ("exit assistant", "exit", "quit"):
        return "exit", None
    if normalized in ("clear screen", "clear"):
        return "clear", None
    if normalized in ("help", "what can you do"):
        return "help", None
    if normalized in ("repeat response", "repeat"):
        return "repeat", None
    if normalized in ("stop listening", "stop"):
        return "stop_listening", None
    if normalized in ("list files", "ls"):
        return "list_files", None
    if normalized in ("show current directory", "pwd", "current directory"):
        return "pwd", None

    # create file <name>
    m = re.match(r"create file\s+(.+)$", normalized)
    if m:
        return "create_file", m.group(1).strip()

    # run python file <name>
    m = re.match(r"run (?:python )?file\s+(.+)$", normalized)
    if m:
        return "run_python", m.group(1).strip()

    # fallback: check for 'run' commands like 'run example.py'
    m = re.match(r"run\s+(.+\.py)$", normalized)
    if m:
        return "run_python", m.group(1).strip()

    return None
