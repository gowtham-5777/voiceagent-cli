# Voice Terminal Agent

A terminal-based voice assistant for interacting with an AI coding agent using speech input.

## Features

- Record microphone audio with push-to-talk.
- Convert speech to text with `faster-whisper`.
-- Send transcribed text to a Groq-backed LLM via an OpenAI-compatible client.
-- Display AI responses in the terminal (formatted with `rich`).
-- Voice and terminal commands: `clear screen`, `create file <name>`, `run python file <name>`, `exit assistant`, `repeat response`, and more.

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

3. Ensure your API key for Groq/OpenAI-compatible access is configured (see below). Install project dependencies:

```bash
pip install -r requirements.txt
```

## Microphone requirement

A working microphone is required for voice input. The project uses `sounddevice` to capture audio.

If the microphone is unavailable, the application provides a text fallback. Use `--text-mode` to start in text-only mode.

## Running the project

Run the assistant from the project root:

```bash
python main.py
```

Start in text-only mode:

```bash
python main.py --text-mode
```

### API Key Setup (required for AI responses)

API Key Setup (required for AI responses)

This project uses an OpenAI-compatible client to reach Groq's API. Set your API key in the environment (example):

```bash
export GROQ_API_KEY="your_api_key_here"
```

You can also add the key to a `.env` file in the project root:

```
GROQ_API_KEY=your_api_key_here
```

If the key is not set the assistant will still run but AI responses will fail.

Workflow:

1. Press ENTER to start recording (push-to-talk).
2. Speak your instruction.
3. Press ENTER again to stop recording.
4. The transcription is sent to the LLM and the formatted response is printed.

## Demo setup time

- Expected setup time: 10–20 minutes.
- The first run may be slower while `faster-whisper` downloads its model.

## Notes

- This project is terminal-only.
- No GUI or text-to-speech is included.
- Keep the voice commands simple and clear for best results.
