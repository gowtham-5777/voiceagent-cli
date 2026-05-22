# Voice Input Interface for a Terminal Coding Agent

## 1. Technology choices

- **Python**: simple, widely available, and the required language for the assignment.
- **faster-whisper**: provides local speech-to-text transcription without a browser-based UI.
- **sounddevice**: captures microphone audio directly with a small dependency set.
- **Open Interpreter**: acts as the terminal-based AI coding agent backend.

## 3. Architecture

The project is organized into clear modules:

- `main.py`: application workflow and user interaction.
- `speech/recorder.py`: microphone recording and push-to-talk control.
- `speech/transcriber.py`: speech-to-text transcription.
- `agent/interpreter_wrapper.py`: Open Interpreter Python API integration.
- `commands/parser.py`: voice command detection.
- `utils/helpers.py`: terminal display helpers.

### Open Interpreter Integration

The wrapper uses Open Interpreter's Python API (`interpreter.chat()`) to send transcribed text and receive AI responses. This avoids subprocess CLI limitations and provides direct access to the interpreter object's methods and configuration.

## 3. Tradeoffs

- **Simplicity over flexibility**: the assistant uses push-to-talk and avoids wake-word detection.
- **Minimal dependency set**: only the packages needed for audio input and transcription were included.
- **Python API over CLI**: Open Interpreter is used via direct Python API calls rather than subprocess invocation, ensuring cleaner error handling and better integration.
- **API key requirement**: The app requires an LLM API key (OpenAI, Anthropic, etc.) to function; it cannot run offline for AI responses.

## 4. Limitations

- The Open Interpreter integration depends on the CLI being installed and available in PATH.
- Speech-to-text quality depends on the chosen Whisper model and microphone quality.
- The code execution command is a placeholder and does not execute arbitrary scripts automatically.

## 5. Future improvements

- Add a local code runner for the `run code` command.
- Expand voice command parsing with more natural language support.
- Improve transcription with a larger Whisper model when hardware allows.
- Add logging and debug modes for smoother development.
