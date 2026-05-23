from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.text import Text
import os
import platform

console = Console()
DEMO_MODE = False


def set_demo_mode(enabled: bool):
    global DEMO_MODE
    DEMO_MODE = enabled


def clear_screen():
    command = "cls" if platform.system() == "Windows" else "clear"
    os.system(command)


def print_header():
    clear_screen()
    console.rule("[bold cyan]VOICE TERMINAL AGENT[/]", style="cyan")
    console.print(Text("Terminal-first voice coding assistant", style="bold green"))
    console.print(Text("Speak coding requests, use terminal commands, and keep demos reliable.", style="dim"))
    console.print()
    console.rule(style="cyan")


def _state(prefix: str, message: str, style: str = "green"):
    console.print(f"{prefix} ", end="")
    console.print(Text(message, style=style))


def print_listening():
    _state("🎤", "Press ENTER and speak...", style="bold magenta")


def print_transcribing():
    _state("📝", "Processing your request...", style="yellow")


def print_thinking():
    _state("🤖", "Thinking...", style="bright_blue")


def print_ready():
    _state("✅", "Response Ready", style="green")


def print_info(message: str):
    console.print(Text(message, style="green"))


def print_debug(message: str):
    if not DEMO_MODE:
        console.print(Text(message, style="dim"))


def print_warning(message: str):
    console.print(Text(message, style="yellow"))


def print_error(message: str):
    console.print(Text(message, style="bold red"))


def print_section(title: str, subtitle: str = ""):
    console.rule(f"[bold cyan]{title}[/] {subtitle}", style="cyan")


def print_response(response: str, title: str = "AI RESPONSE"):
    response = (response or "").strip() or "(no response received)"

    if "```" in response:
        panel = Panel(Markdown(response), title=title, expand=True, style="white on #0b1220")
    elif response.startswith(("def ", "class ", "import ", "from ")) or "\n    " in response:
        syntax = Syntax(response, "python", theme="monokai", line_numbers=False)
        panel = Panel(syntax, title=title, expand=True, style="white on #0b1220")
    elif response.count("\n") >= 2 or response.startswith(('-', '*')):
        panel = Panel(Markdown(response), title=title, expand=True, style="white on #0b1220")
    else:
        panel = Panel(Text(response, overflow="fold"), title=title, expand=True, style="white on #0b1220")

    console.print(panel)


def print_status_list(items: dict):
    lines = []
    for label, status in items.items():
        if any(keyword in status.lower() for keyword in ("found", "loaded", "detected", "ready")):
            lines.append(f"[bold]{label}[/]: [green]✅ {status}[/]")
        else:
            lines.append(f"[bold]{label}[/]: [yellow]⚠️ {status}[/]")
    console.print(Panel(Text("\n".join(lines)), title="Startup Status", expand=True, style="cyan"))


def print_file_result(title: str, content: str):
    panel = Panel(Text(content or "(empty)"), title=title, expand=True, style="green")
    console.print(panel)

