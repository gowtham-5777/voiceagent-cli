import os
import platform

RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"


def clear_screen():
    """Clear the terminal screen."""
    command = "cls" if platform.system() == "Windows" else "clear"
    os.system(command)


def format_text(text: str, color: str = "", bold: bool = False) -> str:
    style = ""
    if bold:
        style += BOLD
    if color:
        style += color
    return f"{style}{text}{RESET}"


def print_header():
    """Print the app header with a simple color theme."""
    clear_screen()
    print(format_text("Voice Terminal Agent", BLUE, bold=True))
    print(format_text("A simple voice input interface for terminal coding workflows.\n", GREEN))


def print_info(message: str):
    print(format_text(message, GREEN))


def print_warning(message: str):
    print(format_text(message, YELLOW))


def print_error(message: str):
    print(format_text(message, RED, bold=True))
