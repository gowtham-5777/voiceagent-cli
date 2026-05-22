from agent.interpreter_wrapper import send_to_open_interpreter
from commands.parser import parse_command
from speech.recorder import record_audio
from speech.transcriber import transcribe_audio
from utils.helpers import clear_screen, print_error, print_header, print_info


def main():
    print_header()
    print_info("Welcome! Press ENTER to begin a voice interaction.")

    while True:
        try:
            audio, samplerate = record_audio()
        except KeyboardInterrupt:
            print_info("Keyboard interrupt received. Exiting assistant.")
            break
        except Exception as exc:
            print_error(f"Recording error: {exc}")
            try:
                fallback_text = input("Type a message instead (or press ENTER to retry): ").strip()
            except EOFError:
                print_error("No fallback input available. Exiting assistant.")
                break
            if not fallback_text:
                continue
            transcription = fallback_text
        else:
            transcription = transcribe_audio(audio, samplerate)

        if not transcription:
            print_error("No transcription was detected. Try again.")
            continue

        print_info(f"You said: {transcription}")
        command = parse_command(transcription)

        if command == "clear":
            clear_screen()
            print_header()
            continue

        if command == "run":
            print_info("Run command received. This is a placeholder for code execution logic.")
            continue

        if command == "exit":
            print_info("Exit command received. Goodbye.")
            break

        response = send_to_open_interpreter(transcription)
        print_info("AI Response:")
        print(response)
        print_info("\nReady for the next command. Press ENTER to start recording again.")

        input()


if __name__ == "__main__":
    main()
