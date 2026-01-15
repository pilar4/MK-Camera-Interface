import speech_recognition as sr
import pyttsx3
import time

# Initialize recognizer and TTS engine once
r = sr.Recognizer()
#engine = pyttsx3.init()

# Keyboard setup
from pynput.keyboard import Key, Controller
keyboard = Controller()

# output keys one by one
def typeKey(text):
    for char in text:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.2)
    return

# Use microphone
with sr.Microphone() as source:
    time.sleep(1)
    print("Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=0.5)
    print("Listening...")

    while True:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio).lower()

            print("You said:", text)

            typeKey(text)

            if text in ("exit", "quit", "stop"):
                break

        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")

        except KeyboardInterrupt:
            print("Program terminated")
            break

import speech_recognition as sr
import pyttsx3
import time

# Initialize recognizer and TTS engine once
r = sr.Recognizer()
#engine = pyttsx3.init()

# Keyboard setup
from pynput.keyboard import Key, Controller
keyboard = Controller()

# output keys one by one
def typeKey(text):
    for char in text:
        keyboard.press(char)
        keyboard.release(char)
        time.sleep(0.12)
    return

# Use microphone
with sr.Microphone() as source:
    time.sleep(0.5)
    print("Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=0.5)
    print("Listening...")

    while True:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio).lower()

            print("You said:", text)

            typeKey(text)

            if text in ("exit", "quit", "stop"):
                break

        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")

        except KeyboardInterrupt:
            print("Program terminated")
            break

