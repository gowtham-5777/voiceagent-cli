# Engineering Report: Voice Terminal Agent

## Motivation

This terminal-first assistant was built to demonstrate a polished voice-driven workflow without adding GUI complexity. The goal was a reliable demo-ready tool that helps developers speak coding requests, execute safe terminal commands, and receive structured output in the same environment they already use.

## Problem statement

Traditional voice assistants are often tied to browsers or mobile apps, which introduces UI overhead and reduces reliability. For a developer-focused demo, the challenge was to deliver a voice interaction loop that stays entirely within the terminal and fails gracefully when audio or LLM connectivity is not available.

## Why terminal-first?

A terminal-first design matters because it keeps the experience lightweight, reduces dependencies, and matches developer workflows. It also avoids brittle GUI layers, lowers the surface area for runtime issues, and makes the assistant easier to demo in live coding sessions.

## Architecture

The solution is intentionally modular:

- `main.py` orchestrates startup checks, command handling, the interaction loop, and fallback behavior.
- `speech/recorder.py` handles push-to-talk audio capture and microphone availability checks.
- `speech/transcriber.py` loads `faster-whisper` once and performs transcription.
- `agent/llm_client.py` sends user requests to Groq via an OpenAI-compatible client.
- `commands/parser.py` maps spoken or typed text to safe assistant commands.
- `utils/helpers.py` renders a clean terminal UI with panels, status feedback, and formatted responses.
- `utils/session.py` stores the last user command and last AI response for repeatability.

## Technology decisions

- **Python**: simple, portable, and easy to reason about.
- **sounddevice**: reliable terminal microphone capture without a GUI.
- **faster-whisper**: efficient local transcription with reusable model state.
- **Groq API**: provides a performant LLM backend compatible with existing OpenAI-style clients.
- **rich**: creates polished terminal rendering without browser dependencies.
- **python-dotenv**: keeps API configuration secure and easy to manage.

## Why faster-whisper?

`faster-whisper` was selected for its balance of performance and transcription quality. Its single-model reuse pattern keeps repeated voice requests responsive and avoids reloading overhead on each interaction.

## Why Groq API?

Groq offers a modern LLM backend with a clean, OpenAI-compatible API surface. This made it straightforward to keep the assistant architecture simple and terminal-focused while still using a powerful model.

## Why replace Open Interpreter?

Open Interpreter was removed to avoid an extra wrapper layer and unnecessary dependency complexity. A direct Groq client integration simplifies the code path, reduces potential points of failure, and improves maintainability.

## Agent Architecture Decision

Initially, the system was designed as a wrapper around Open Interpreter to directly integrate with an existing terminal-based coding agent. During implementation, dependency instability and compatibility issues introduced reliability concerns that negatively impacted live demo stability.

To prioritize maintainability, modularity, and consistent terminal interaction behavior, the architecture was refactored into a self-contained terminal voice coding assistant powered directly by the Groq LLM API.

This approach preserved the core objective of the assignment:
- voice-driven terminal interaction
- reduced keyboard usage
- coding-oriented assistance
- terminal-first workflow

while significantly improving:
- reliability
- response consistency
- demo readiness
- modular architecture

The final system behaves as a lightweight terminal coding assistant optimized for voice-first interaction rather than as a thin wrapper around a third-party terminal agent.

## Tradeoffs

- The assistant is intentionally not a full IDE or sandboxed execution environment.
- It favors terminal reliability and clarity over broad voice command coverage.
- The current implementation uses CPU-safe transcription by default, which is slower but portable.

## Reliability decisions

- Added clear startup diagnostics for `.env`, API key, microphone, and transcription readiness.
- Suppressed noisy library warnings so demo output remains clean.
- Implemented safe filename validation to prevent path traversal during file creation and execution.
- Added typed fallback and `--text-mode` to handle missing audio hardware.
- Cleanly handled keyboard interrupts and prevented raw tracebacks from appearing in normal use.

## Limitations

- The assistant still requires network access for Groq LLM responses.
- Local code execution is limited to simple Python files in the current directory.
- Voice transcription quality depends on ambient noise and microphone clarity.

## Future improvements

- Add richer natural language command parsing and more aliases.
- Add command history and clearer intent confirmation.
- Introduce an optional safe sandbox for local code execution.
- Improve onboarding prompts for first-time users.

## API cost analysis

Groq API cost considerations:

- Groq provides low-latency inference suitable for live demos; check Groq's current pricing for exact rates.
- Cost formula: `cost_per_request = (avg_tokens / 1000) * cost_per_1k_tokens`.
	- Example (adjust to current pricing): with `avg_tokens = 500` and `cost_per_1k_tokens = $0.02`, `cost_per_request = (500/1000)*0.02 = $0.01`; 100 demo requests ≈ $1.
- Mitigations: limit `max_tokens`, keep the system prompt concise, prefer short responses in demo mode, cache frequent replies, and rate-limit/demo quotas to control spend.

## Demo experience

The final design is intended for a smooth live demo: a strong startup status screen, a single clean prompt for voice input, safe terminal commands, and formatted AI responses presented in panels. This keeps the assistant feeling professional, reliable, and easy to present.
