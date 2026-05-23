import argparse
import os
import subprocess
import sys

from dotenv import load_dotenv

from agent.llm_client import send_to_llm
from speech import recorder, transcriber
from commands import parser as cmd_parser
from utils import helpers, session


# Load env
load_dotenv()


ALLOWED_EXT = {".py", ".txt", ".md"}


def _is_safe_path(base_dir: str, path: str) -> bool:
    # Prevent path traversal: ensure normalized path starts with base_dir
    abs_base = os.path.abspath(base_dir)
    dest = os.path.abspath(os.path.join(base_dir, path))
    return os.path.commonpath([abs_base]) == os.path.commonpath([abs_base, dest])


def _create_file(base_dir: str, filename: str) -> str:
    name = filename.strip()
    if not name:
        return "Invalid filename."
    root, ext = os.path.splitext(name)
    if ext not in ALLOWED_EXT:
        return f"Extension '{ext}' is not allowed. Use .py, .txt, or .md"
    if not _is_safe_path(base_dir, name):
        return "Unsafe filename (path traversal detected)."
    path = os.path.join(base_dir, name)
    if os.path.exists(path):
        return f"File already exists: {path}"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("")
    return f"Created file: {path}"


def _run_python_file(base_dir: str, filename: str) -> str:
    name = filename.strip()
    if not name:
        return "Invalid filename."
    if not _is_safe_path(base_dir, name):
        return "Unsafe filename (path traversal detected)."
    path = os.path.join(base_dir, name)
    if not os.path.exists(path):
        return f"File not found: {path}"
    try:
        result = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=30)
        output = result.stdout or result.stderr
        return output or f"Ran {path} (no output)."
    except Exception as exc:
        return f"Error running file: {exc}"


def run_assistant(text_mode: bool = False):
    base_dir = os.getcwd()
    helpers.print_header()
    helpers.print_info("Starting Voice Terminal Agent. Press Ctrl+C to exit.")

    try:
        while True:
            # Get input: voice or text
            transcription = None
            if text_mode:
                user_input = input("Type your command or message: ")
                transcription = user_input.strip()
            else:
                try:
                    helpers.print_listening()
                    audio, sr = recorder.record_audio()
                    helpers.print_transcribing()
                    transcription = transcriber.transcribe_audio(audio, sr)
                except Exception as exc:
                    helpers.print_warning(f"Microphone unavailable or recording failed: {exc}")
                    user_input = input("Microphone unavailable. Type your command: ")
                    transcription = user_input.strip()

            if not transcription:
                continue

            cmd = cmd_parser.parse_command(transcription)
            if cmd:
                action, arg = cmd
                if action == "exit":
                    helpers.print_info("👋 Exiting Voice Terminal Agent...")
                    break
                if action == "clear":
                    helpers.clear_screen()
                    continue
                if action == "help":
                    helpers.print_info("Commands: exit assistant, clear screen, help, repeat response, list files, show current directory, create file <name>, run python file <name>")
                    continue
                if action == "repeat":
                    last = session.get_last_response()
                    if last:
                        helpers.print_response(last)
                    else:
                        helpers.print_info("No previous response to repeat.")
                    continue
                if action == "list_files":
                    files = os.listdir(base_dir)
                    helpers.print_response("\n".join(files), title="FILES")
                    continue
                if action == "pwd":
                    helpers.print_response(base_dir, title="CWD")
                    continue
                if action == "create_file":
                    result = _create_file(base_dir, arg)
                    helpers.print_info(result)
                    continue
                if action == "run_python":
                    out = _run_python_file(base_dir, arg)
                    helpers.print_response(out or "", title=f"Run: {arg}")
                    continue

            # If not a command, send to LLM
            helpers.print_thinking()
            response = send_to_llm(transcription)
            helpers.print_ready()
            helpers.print_response(response)
            session.store_last_response(response)

    except KeyboardInterrupt:
        helpers.print_info("👋 Exiting Voice Terminal Agent...")


def main():
    parser = argparse.ArgumentParser(description="Voice Terminal Assistant")
    parser.add_argument("--text-mode", action="store_true", help="Start in text-only mode (typed input)")
    args = parser.parse_args()

    run_assistant(text_mode=args.text_mode)


if __name__ == "__main__":
    main()