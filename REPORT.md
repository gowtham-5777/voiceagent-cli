# Engineering Report: Voice Terminal Agent

## Motivation

This project was developed as a terminal-first voice coding assistant for internship evaluation. The goal was to keep the experience professional and reliable while minimizing keyboard interaction and avoiding frontend complexity.

## Why terminal-first?

A terminal-based design is ideal for coding workflows because it matches a developer's natural environment, reduces UI surface area, and improves demo reliability. It avoids browser or GUI dependencies and keeps the assistant lightweight and focused.

## Architecture

The assistant is modular and cleanly separated:

- `main.py` contains the controller, startup validation, CLI flags, command handling, and session state.
- `speech/recorder.py` manages microphone capture with push-to-talk reliability.
- `speech/transcriber.py` manages `faster-whisper` transcription with singleton model reuse.
- `agent/llm_client.py` sends prompts to a Groq-hosted LLM via an OpenAI-compatible client.
- `commands/parser.py` identifies voice and typed commands.
- `utils/helpers.py` renders rich terminal states and formatted responses.
- `utils/session.py` stores the last AI response and last user command in memory.

## Technology choices

- **Python**: chosen for simplicity, portability, and familiarity.
- **sounddevice**: provides direct microphone capture in the terminal.
- **faster-whisper**: offers efficient speech-to-text transcription with local model reuse.
- **Groq API**: used for LLM responses via OpenAI-compatible calls.
- **rich**: delivers polished terminal formatting without GUI dependencies.
- **python-dotenv**: manages environment configuration cleanly.

## Why faster-whisper?

`faster-whisper` provides a good balance between offline transcription quality and performance. Its ability to load a model once and reuse it lowers latency for repeated voice requests.

## Why Groq API?

Groq provides a modern LLM backend with an OpenAI-compatible interface. This project uses the existing Python-compatible client pattern for direct API calls and clean integration.

## Why remove Open Interpreter?

The architecture was simplified to avoid stale dependencies and wrapper layers. The assistant now communicates directly with the Groq API client, which reduces indirection and improves maintainability.

## Engineering decisions

- **Reliability over novelty**: push-to-talk is kept for stability instead of experimental always-listening behavior.
- **Demo mode**: added a lightweight presentation mode to reduce noise and highlight essential status output.
- **Startup validation**: added runtime checks for the microphone, `.env`, API key, and whisper model.
- **Session memory**: retained the last AI response and last user command for repeatability.
- **Safe command execution**: filename validation prevents path traversal and restricts file creation to `.py`, `.txt`, and `.md`.
- **Modular code**: each responsibility is isolated to one module to keep the codebase understandable and beginner-friendly.

## Reliability improvements

- Suppressed noisy library warnings during demo mode.
- Added clear startup diagnostics and friendly fallback behavior.
- Improved command handling and error messages.
- Avoided tracebacks for normal user errors and interruptions.

## Limitations

- The assistant still requires a network connection for LLM responses.
- It is not a fully sandboxed code execution environment.
- Transcription quality depends on microphone clarity and acoustic conditions.

## Future improvements

- Add richer support for natural voice command variations.
- Add optional local command history or command review.
- Add an explicit safe mode for file execution output.

## Demo readiness

This project is engineered for a stable live demo with clear terminal output, strong fallback behavior, and a polished command-driven assistant experience.
