# commands.py
import os
import subprocess
import datetime
import pywhatkit
from PIL import Image, ImageTk, Image, ImageDraw, ImageFilter  # keep for avatar if needed
import ctypes
import time

import core  # our shared utilities

# Windows virtual key codes for volume (simple helpers using ctypes)
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

def _press_key(vk_code):
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

def volume_up(steps=3):
    for _ in range(steps):
        _press_key(VK_VOLUME_UP)
    core.say("Increasing volume, sir.")

def volume_down(steps=3):
    for _ in range(steps):
        _press_key(VK_VOLUME_DOWN)
    core.say("Decreasing volume, sir.")

def mute_volume():
    _press_key(VK_VOLUME_MUTE)
    core.say("Toggling mute, sir.")

def lock_pc():
    core.say("Locking your computer, sir.")
    ctypes.windll.user32.LockWorkStation()

# Media functions
def playMusic():
    music_path = r"C:\Users\ANKIT\Documents\Semparo.mp4"
    if os.path.exists(music_path):
        os.startfile(music_path)
        core.say("Playing music, sir...")
    else:
        core.say("I could not find your music file, sir.")

def play_youtube_song():
    core.say("What should I play on YouTube, sir?")
    song = core.takeCommand()
    if song:
        core.say(f"Playing {song} on YouTube, sir...")
        try:
            pywhatkit.playonyt(song)
        except Exception as e:
            print("play_youtube error:", e)
            core.say("I'm sorry sir, I could not play that on YouTube.")
    else:
        core.say("I did not catch the name of the song, sir.")

# WhatsApp
def send_whatsapp_message():
    contacts = {
        "abhijeet": "+919692991957",
        "snorlax": "+919692977283",
        "swayam": "+917750941501",
        "mummy": "+917979844814",
    }
    core.say("Whom do you want to send a message, sir?")
    name = core.takeCommand()
    if name and name.lower() in contacts:
        number = contacts[name.lower()]
        core.say(f"What is the message for {name}, sir?")
        message = core.takeCommand()
        if message:
            core.say(f"Sending message to {name}...")
            try:
                pywhatkit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
                core.say("Message sent, sir.")
            except Exception as e:
                print("WhatsApp error:", e)
                core.say("I'm sorry sir, I couldn't send the message.")
    else:
        core.say("I couldn't find that contact in your list.")

# System controls (shutdown etc.)
def shutdown_system():
    core.say("Shutting down now, sir.")
    subprocess.Popen(["shutdown", "/s", "/t", "0"])

def restart_system():
    core.say("Restarting now, sir.")
    subprocess.Popen(["shutdown", "/r", "/t", "0"])

def sign_out():
    core.say("Signing out now, sir.")
    subprocess.Popen(["shutdown", "/l"])

def sleep_system():
    core.say("Putting system to sleep, sir.")
    subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])

# Screenshot
from PIL import ImageGrab
def take_screenshot(save_dir=r"C:\Users\ANKIT\Pictures"):
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(save_dir, f"screenshot_{ts}.png")
    img = ImageGrab.grab()
    img.save(path)
    core.say(f"Screenshot saved to {path}, sir.")
    return path

# Handle query (moved from main)
def handle_query(query: str):
    if not query:
        return "ok"
    q = query.lower()

    # EXIT
    if "exit" in q or "quit" in q or "goodbye" in q or "bye light" in q:
        core.say("Goodbye sir. Shutting down.")
        return "exit"

    # Basic commands
    if "play music" in q:
        playMusic()
    elif "the time" in q or "what time" in q:
        time_str = datetime.datetime.now().strftime("%I:%M %p")
        core.say(f"The time is {time_str}, sir.")
    elif "open vs code" in q or "open visual studio code" in q:
        try:
            subprocess.Popen(r"C:\Users\ANKIT\AppData\Local\Programs\Microsoft VS Code\Code.exe")
            core.say("Opening VS Code, sir.")
        except Exception as e:
            print(e)
            core.say("I could not open VS Code, sir.")
    elif "open chrome" in q:
        try:
            subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
            core.say("Opening Chrome, sir.")
        except Exception as e:
            print(e)
            core.say("I could not open Chrome, sir.")
    elif "increase volume" in q or "volume up" in q:
        volume_up()
    elif "decrease volume" in q or "volume down" in q:
        volume_down()
    elif "mute" in q and "volume" in q or q.strip() == "mute":
        mute_volume()
    elif "lock my pc" in q or "lock the computer" in q:
        lock_pc()
    elif "my idol" in q:
        core.say("Your idol is Cristiano Ronaldo, sir.")
    elif "best player" in q:
        core.say("The best player in the world is Cristiano Ronaldo, sir.")
    elif "anime character" in q:
        core.say("The best anime character is Son Goku, sir.")
    elif "play song on youtube" in q or "play on youtube" in q:
        play_youtube_song()
    elif "send message" in q or "send whatsapp" in q:
        send_whatsapp_message()
    elif "brightness up" in q or "increase brightness" in q or "increase more" in q:
        core.increase_brightness()
    elif "brightness down" in q or "decrease brightness" in q or "decrease more" in q:
        core.decrease_brightness()
    elif "light search" in q:
        prompt = q.replace("light search", "").strip()
        if not prompt:
            core.say("What should I search for, sir?")
            followup = core.takeCommand()
            if followup:
                prompt = followup
        if prompt:
            answer = core.ai(prompt)
            print(answer)
            core.say(answer)
        else:
            core.say("I did not get what to search for, sir.")
    else:
        # try open common sites
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "http://www.wikipedia.com"],
            ["google", "http://www.google.com"],
            ["instagram", "https://www.instagram.com"],
        ]
        matched = False
        for site in sites:
            if site[0] in q:
                core.say(f"Opening {site[0]}, sir.")
                subprocess.Popen(["start", site[1]], shell=True)
                matched = True
                break
        if not matched:
            core.say("Let me think about that, sir.")
            answer = core.ai(q)
            print(answer)
            core.say(answer)

    return "ok"
