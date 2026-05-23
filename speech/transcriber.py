try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None

from utils.helpers import print_debug, print_error


model = None


def load_model(model_size: str = "tiny.en", device: str = "cpu"):
    """Load the speech-to-text model once and reuse it."""
    global model
    if WhisperModel is None:
        raise RuntimeError(
            "The 'faster-whisper' package is not installed. "
            "Install it with 'pip install faster-whisper' or 'pip install -r requirements.txt'."
        )
    if model is None:
        print_debug("Loading faster-whisper model. This may take a moment on first run.")
        model = WhisperModel(model_size, device=device)
    return model


def transcribe_audio(audio, samplerate: int):
    """Convert recorded audio into text using faster-whisper."""
    model = load_model()
    try:
        segments, _ = model.transcribe(audio, beam_size=5, language="en")
        transcription = " ".join(segment.text for segment in segments).strip()
        return transcription
    except Exception as exc:
        print_error(f"Transcription error: {exc}")
        return ""
