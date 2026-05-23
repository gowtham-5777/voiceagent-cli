import argparse
import logging
import os
import subprocess
import sys
import warnings
from pathlib import Path

from dotenv import load_dotenv

from agent.llm_client import send_to_llm
from commands import parser as cmd_parser
from speech import recorder, transcriber
from utils import helpers, session

# Suppress noisy third-party warnings for clean demo output.
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("ctranslate2").setLevel(logging.ERROR)
logging.getLogger("faster_whisper").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning)

# Load environment variables
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


def _startup_status(text_mode: bool) -> dict:
    status = {
        ".env file": "found" if Path(".env").exists() else "missing",
        "Groq API key": "loaded" if os.getenv("GROQ_API_KEY") else "missing",
    }

    if text_mode:
        status["Microphone"] = "skipped (text-only mode)"
        status["Whisper model"] = "skipped (text-only mode)"
    else:
        try:
            recorder.is_microphone_available()
            status["Microphone"] = "detected"
        except Exception as exc:
            status["Microphone"] = f"unavailable ({exc})"

        try:
            transcriber.load_model()
            status["Whisper model"] = "ready"
        except Exception as exc:
            status["Whisper model"] = f"unavailable ({exc})"

    return status


def _display_startup_status(status: dict):
    helpers.print_section("STARTUP STATUS")
    helpers.print_status_list(status)
    helpers.print_info("Ready for voice or typed commands. Use --demo for cleaner display.")


def run_assistant(text_mode: bool = False, demo_mode: bool = False):
    base_dir = os.getcwd()
    helpers.set_demo_mode(demo_mode)
    helpers.print_header()
    status = _startup_status(text_mode)
    _display_startup_status(status)

    if not text_mode and status.get("Microphone", "") != "detected":
        helpers.print_warning("Voice input is unavailable. Falling back to text-only mode.")
        text_mode = True

    if not text_mode and status.get("Whisper model", "") != "ready":
        helpers.print_warning("Whisper model is unavailable. Falling back to text-only mode.")
        text_mode = True

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
                except KeyboardInterrupt:
                    raise
                except Exception as exc:
                    helpers.print_warning(f"Voice capture failed: {exc}")
                    transcription = input("Type your command instead: ").strip()

            if not transcription:
                continue

            session.store_last_command(transcription)
            cmd = cmd_parser.parse_command(transcription)
            if cmd:
                action, arg = cmd
                if action == "exit":
                    helpers.print_info("👋 Exiting Voice Terminal Agent...")
                    break
                if action == "clear":
                    helpers.clear_screen()
                    helpers.print_header()
                    continue
                if action == "help":
                    helpers.print_response(
                        "Available commands:\n"
                        "- exit assistant\n"
                        "- clear screen\n"
                        "- help\n"
                        "- repeat response\n"
                        "- list files\n"
                        "- show current directory\n"
                        "- create file <filename>\n"
                        "- run python file <filename>",
                        title="COMMANDS"
                    )
                    continue
                if action == "repeat":
                    last = session.get_last_response()
                    if last:
                        helpers.print_response(last, title="LAST RESPONSE")
                    else:
                        helpers.print_info("No previous AI response available.")
                    continue
                if action == "list_files":
                    files = os.listdir(base_dir)
                    helpers.print_file_result("FILES", "\n".join(files))
                    continue
                if action == "pwd":
                    helpers.print_file_result("CURRENT DIRECTORY", base_dir)
                    continue
                if action == "create_file":
                    result = _create_file(base_dir, arg)
                    helpers.print_info(result)
                    continue
                if action == "run_python":
                    out = _run_python_file(base_dir, arg)
                    helpers.print_response(out or "", title=f"RUN {arg}")
                    continue

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
    parser.add_argument("--demo", action="store_true", help="Enable demo mode with cleaner terminal output")
    args = parser.parse_args()

    run_assistant(text_mode=args.text_mode, demo_mode=args.demo)


if __name__ == "__main__":
    main()