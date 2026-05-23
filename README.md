# Voice Terminal Agent

A polished terminal-first voice coding assistant for reliable developer workflows.

## Overview

`voiceagent-cli` turns spoken coding requests into terminal-ready responses with a push-to-talk workflow. It combines microphone capture, local transcription, and Groq-backed LLM results in a clean, demo-ready terminal experience.

## Architecture

```text
Microphone
  ↓
sounddevice recording
  ↓
faster-whisper transcription
  ↓
Groq LLM API
  ↓
Rich terminal rendering
```

## Key features

- Push-to-talk voice capture with a clean single prompt.
- `faster-whisper` transcription with a reused model instance.
- Groq OpenAI-compatible LLM integration using `llama-3.3-70b-versatile`.
- Rich terminal interface powered by `rich`.
- Text-only mode for reliable fallbacks.
- Demo mode for polished output.
- Safe command execution for file creation and script runs.

## Getting started

1. Create a virtual environment and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your Groq key:

   ```bash
   cp .env.example .env
   ```

4. Edit `.env`:

   ```text
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Running the assistant

Start in voice mode:

```bash
python main.py
```

Start in typed mode:

```bash
python main.py --text-mode
```

Start in demo mode:

```bash
python main.py --demo
```

## Voice interaction

The assistant uses a single clean prompt for voice input:

- `🎤 Press ENTER and speak...`

Use these voice commands directly:

- `exit assistant`
- `clear screen`
- `help`
- `repeat response`
- `stop listening`
- `resume listening`
- `list files`
- `show current directory`
- `create file <filename>`
- `run python file <filename>`

## Terminal commands

In text mode or fallback mode you can type:

- `list files`
- `show current directory`
- `create file notes.txt`
- `run python file script.py`
- `clear screen`
- `repeat response`
- `help`
- `exit assistant`

## Example terminal flow

```text
================================
VOICE TERMINAL AGENT
================================
✅ .env loaded
✅ Groq API key loaded
✅ Microphone detected
✅ Whisper model ready
✅ Terminal assistant initialized

Ready for voice interaction.
```

## Troubleshooting

- If `GROQ_API_KEY` is missing, the assistant will report the issue and still allow local terminal commands.
- If the microphone is unavailable, the app automatically falls back to text-only mode.
- The first run may take longer while the `faster-whisper` model loads.

## Limitations

- Terminal-only experience, no GUI or browser interface.
- Requires network access for LLM responses.
- Code execution is intentionally limited to simple Python scripts in the current working directory.

## Future improvements

- Add more natural voice command variations.
- Improve command history and interactive help.
- Add optional safe sandboxing for local code execution.
- Add better command aliases and voice command parsing.

## Project files

- `main.py` — app orchestration, startup diagnostics, and command loop.
- `speech/recorder.py` — microphone recording and push-to-talk control.
- `speech/transcriber.py` — faster-whisper model loading and audio transcription.
- `agent/llm_client.py` — Groq LLM request handling.
- `commands/parser.py` — voice and typed command parsing.
- `utils/helpers.py` — polished terminal rendering.
- `utils/session.py` — last-response memory.
