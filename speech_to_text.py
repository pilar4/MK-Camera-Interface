import speech_recognition as sr
import pyttsx3

# Initialize recognizer and TTS engine once
r = sr.Recognizer()
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Use microphone
with sr.Microphone() as source:
    print("Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=0.5)
    print("Listening...")

    while True:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio).lower()

            print("You said:", text)
            speak_text(text)

            if text in ("exit", "quit", "stop"):
                speak_text("Goodbye")
                break

        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")

        except KeyboardInterrupt:
            print("Program terminated")
            break
