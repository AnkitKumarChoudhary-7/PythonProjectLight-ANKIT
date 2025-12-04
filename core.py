# core.py
import os
import datetime
from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr
from openai import OpenAI
import screen_brightness_control as sbc

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

import pyttsx3


def say(text: str):
    """Speak the given text aloud."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Select a different voice if more than one is available
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)

    print(f"Light says: {text}")
    engine.say(text)
    engine.runAndWait()


# ---------- AI (very small wrapper) ----------
chat_history = [
    {
        "role": "system",
        "content": (
            "You are Light, a helpful, concise voice assistant running on Ankit's Windows PC. "
            "Keep answers short and clear, speak like a friendly AI companion."
        ),
    }
]

def ai(prompt: str) -> str:
    global chat_history
    messages = chat_history + [{"role": "user", "content": prompt}]
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        answer = response.choices[0].message.content
        chat_history.append({"role": "user", "content": prompt})
        chat_history.append({"role": "assistant", "content": answer})
        # Keep history short
        if len(chat_history) > 20:
            chat_history = [chat_history[0]] + chat_history[-18:]
        return answer
    except Exception as e:
        print("AI error:", e)
        return "Sorry sir, I had trouble thinking just now."

# ---------- Speech recognition ----------
def takeCommand():
    """Listen and return recognized text (or None)."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Couldn't understand audio.")
        say("Sorry, I couldn't understand. Please say that again.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        say("There was a problem with the speech service, sir.")
        return None
    except Exception as e:
        print("Unexpected error in takeCommand:", e)
        return None

# ---------- Brightness helpers using screen_brightness_control ----------
def set_brightness(percent: int):
    try:
        sbc.set_brightness(percent)
        say(f"Brightness set to {percent} percent, sir.")
    except Exception as e:
        print("set_brightness error:", e)
        say("I couldn't change brightness, sir.")

def get_brightness():
    try:
        return sbc.get_brightness()[0]
    except Exception as e:
        print("get_brightness error:", e)
        return None

def increase_brightness(step: int = 10):
    try:
        current = get_brightness() or 0
        new_level = min(100, current + step)
        sbc.set_brightness(new_level)
        say(f"Brightness increased to {new_level} percent, sir.")
    except Exception as e:
        print("increase_brightness error:", e)
        say("I couldn't increase brightness, sir.")

def decrease_brightness(step: int = 10):
    try:
        current = get_brightness() or 0
        new_level = max(0, current - step)
        sbc.set_brightness(new_level)
        say(f"Brightness decreased to {new_level} percent, sir.")
    except Exception as e:
        print("decrease_brightness error:", e)
        say("I couldn't decrease brightness, sir.")
