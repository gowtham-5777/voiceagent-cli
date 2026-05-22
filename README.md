# Voice Terminal Agent

A terminal-based voice assistant for interacting with an AI coding agent using speech input.

## Features

- Record microphone audio with push-to-talk.
- Convert speech to text with `faster-whisper`.
- Send transcribed text to Open Interpreter.
- Display AI responses in the terminal.
- Basic voice commands: `clear screen`, `run code`, `exit assistant`.

## Installation

1. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install Open Interpreter separately if the CLI is not already available:

   ```bash
   pip install open-interpreter
   ```

   If the command is not found, the app can also use the installed `interpreter` CLI entrypoint.

## Microphone requirement

A working microphone is required for voice input. The project uses `sounddevice` to capture audio.

If the microphone is unavailable, the application provides a text fallback.

## Running the project

Run the assistant from the project root:

```bash
python main.py
```

### API Key Setup (required for AI responses)

Before using Open Interpreter, set your API provider's credentials:

**OpenAI (recommended):**

```bash
export OPENAI_API_KEY="sk-..."
python main.py
```

Or use other supported providers by setting the appropriate environment variables (e.g., `ANTHROPIC_API_KEY` for Claude).

**Note:** Open Interpreter defaults to OpenAI's GPT models. If you don't have credentials, the app will fail when attempting to send requests to the AI.

Workflow:

1. Press ENTER to start recording (or speak).
2. Speak your instruction.
3. Press ENTER again to stop recording.
4. The transcription is sent to Open Interpreter via Python API.
5. Read the AI response in the terminal.

## Demo setup time

- Expected setup time: 10–20 minutes.
- The first run may be slower while `faster-whisper` downloads its model.

## Notes

- This project is terminal-only.
- No GUI or text-to-speech is included.
- Keep the voice commands simple and clear for best results.
