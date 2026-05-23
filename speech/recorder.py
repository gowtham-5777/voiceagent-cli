import threading

import numpy as np

from utils.helpers import print_error, print_info

try:
    import sounddevice as sd
except ImportError:
    sd = None


def _find_input_device(samplerate: int, channels: int):
    """Return a usable input device index or raise if none is available."""
    try:
        devices = sd.query_devices()
    except Exception as exc:
        raise RuntimeError(
            "Unable to query audio devices. "
            "Make sure a microphone is connected and available to the system. "
            f"({exc})"
        ) from exc

    input_devices = [
        (idx, device)
        for idx, device in enumerate(devices)
        if device.get("max_input_channels", 0) >= channels
    ]

    if not input_devices:
        raise RuntimeError(
            "No input audio device was found. "
            "Please connect a microphone and try again."
        )

    last_error = None
    for idx, device in input_devices:
        try:
            sd.check_input_settings(device=idx, channels=channels, samplerate=samplerate, dtype="float32")
            return idx
        except Exception as exc:
            last_error = exc

    raise RuntimeError(
        "Unable to open any available input device. "
        "Please verify your microphone and system audio settings. "
        f"Last error: {last_error}"
    ) from last_error


def is_microphone_available(samplerate: int = 16000, channels: int = 1) -> bool:
    """Return whether a valid microphone input device is available."""
    if sd is None:
        raise RuntimeError(
            "The 'sounddevice' package is not installed. "
            "Install it with 'pip install sounddevice' or 'pip install -r requirements.txt'."
        )
    _find_input_device(samplerate=samplerate, channels=channels)
    return True


def record_audio(samplerate: int = 16000, channels: int = 1):
    """Record audio from the microphone until the user presses ENTER again."""
    frames = []
    stop_event = threading.Event()

    def stop_listener():
        input()
        stop_event.set()

    def audio_callback(indata, frames_count, time, status):
        if status:
            print_error(f"Microphone warning: {status}")
        frames.append(indata.copy())
        if stop_event.is_set():
            raise sd.CallbackStop()

    if sd is None:
        raise RuntimeError(
            "The 'sounddevice' package is not installed. "
            "Install it with 'pip install sounddevice' or 'pip install -r requirements.txt'."
        )

    device_index = _find_input_device(samplerate=samplerate, channels=channels)

    print_info("Press ENTER to begin speaking. Press ENTER again when finished.")
    input()
    print_info("Recording... speak now.")

    listener = threading.Thread(target=stop_listener, daemon=True)
    listener.start()

    try:
        with sd.InputStream(
            samplerate=samplerate,
            channels=channels,
            dtype="float32",
            callback=audio_callback,
            device=device_index,
        ):
            while not stop_event.is_set():
                sd.sleep(100)
    except Exception as exc:
        raise RuntimeError(f"Recording failed: {exc}") from exc

    if not frames:
        raise RuntimeError("No audio was captured. Try again.")

    audio = np.concatenate(frames, axis=0)
    if channels == 1 and audio.ndim > 1:
        audio = np.squeeze(audio, axis=1)

    return audio, samplerate
