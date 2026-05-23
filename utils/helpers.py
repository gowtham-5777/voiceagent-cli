from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import os
import platform

console = Console()


def clear_screen():
    command = "cls" if platform.system() == "Windows" else "clear"
    os.system(command)


def print_header():
    clear_screen()
    console.print(Panel(Text("Voice Terminal Agent", justify="center", style="bold cyan"), subtitle="Terminal coding assistant", expand=False))


def _state(prefix: str, message: str, style: str = "green"):
    console.print(f"{prefix} ", end="")
    console.print(Text(message, style=style))


def print_listening():
    _state("🎤", "Listening...", style="bold magenta")


def print_transcribing():
    _state("📝", "Transcribing...", style="yellow")


def print_thinking():
    _state("🤖", "Thinking...", style="bright_blue")


def print_ready():
    _state("✅", "Response Ready", style="green")


def print_info(message: str):
    console.print(Text(message, style="green"))


def print_warning(message: str):
    console.print(Text(message, style="yellow"))


def print_error(message: str):
    console.print(Text(message, style="bold red"))


def print_response(response: str, title: str = "AI RESPONSE"):
    panel = Panel(response, title=title, expand=True, style="white on #0b1220")
    console.print(panel)

