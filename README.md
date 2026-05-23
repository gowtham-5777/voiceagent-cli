# Voice Terminal Agent

A terminal-first voice coding assistant for reliable developer workflows.

## Overview

This project offers a polished, terminal-only voice assistant that converts spoken coding requests into text, sends them to a Groq-backed LLM, and displays formatted AI responses directly in the terminal.

## Architecture

User voice → `sounddevice` microphone capture → `faster-whisper` transcription → Groq LLM API → terminal response

## Features

- Push-to-talk voice capture with microphone fallback.
- `faster-whisper` transcription with single-model reuse.
- OpenAI-compatible Groq LLM integration.
- Rich terminal UI with status states and panels.
- Text-only mode (`--text-mode`).
- Demo mode (`--demo`) for cleaner presentation.
- Secure terminal commands: `list files`, `show current directory`, `create file <filename>`, `run python file <filename>`.
- Voice commands: `exit assistant`, `clear screen`, `help`, `repeat response`, `stop listening`.

## Setup

1. Create a virtual environment and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your Groq API key to a `.env` file in the project root:

   ```text
   GROQ_API_KEY=your_api_key_here
   ```

   Or export it in your shell:

   ```bash
   set GROQ_API_KEY="your_api_key_here"
   ```

## Running the assistant

Normal voice mode:

```bash
python main.py
```

Text-only mode:

```bash
python main.py --text-mode
```

Demo mode:

```bash
python main.py --demo
```

Demo mode reduces non-essential output and highlights terminal readability.

## Voice commands

Speak one of the following commands directly:

- `exit assistant`
- `clear screen`
- `help`
- `repeat response`
- `stop listening`
- `list files`
- `show current directory`
- `create file <filename>`
- `run python file <filename>`

## Terminal commands

Type input directly in text mode or when voice capture is unavailable.

Supported commands:

- `list files`
- `show current directory`
- `create file notes.txt`
- `run python file script.py`
- `clear screen`
- `repeat response`
- `help`
- `exit assistant`

## Troubleshooting

- If `GROQ_API_KEY` is missing, AI responses will fail, but the assistant can still run for local command handling.
- If the microphone is unavailable, the assistant will fall back to typed input.
- The first run may take longer while `faster-whisper` loads its model.

## Limitations

- This project is intentionally terminal-only.
- It does not include GUI or browser-based interfaces.
- LLM responses depend on network access and valid API credentials.

## Future improvements

- Add a richer local command palette.
- Improve voice command parsing with more natural language variations.
- Add an optional safe code sandbox for local script execution.

## Demo setup time

- Estimated setup: 10–20 minutes.
- First run model load may take longer; subsequent runs are faster.
