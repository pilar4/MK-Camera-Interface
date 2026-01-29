import speech_recognition as sr
import time



# Keyboard setup
from pynput.keyboard import Key, Controller
keyboard = Controller()

# output keys one by one
def typeKey(text):
    for char in text:
        keyboard.press(char)
        keyboard.release(char)
        delay = 0.05 if len(text) > 10 else 0.12
        time.sleep(delay)

    return

def speech_worker(text_queue, stop_event):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        time.sleep(0.5)
        print("Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")

        while not stop_event.is_set():
            try:
                audio = r.listen(source, timeout=1)
                text = r.recognize_google(audio).lower()

                print("You said:", text)

                typeKey(text)

                if text in ("exit", "quit", "stop"):
                    break

            except sr.WaitTimeoutError:
                continue

            except sr.UnknownValueError:
                print("Could not understand audio")

            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")

            except KeyboardInterrupt:
                print("Program terminated")
                break