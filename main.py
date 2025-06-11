import speech_recognition as sr
import pyttsx3 as ts
import webbrowser as browse
from queue import Queue
from threading import Thread
import os
import pyautogui

tts = ts.init()
tts.setProperty('rate', 170)

def speak(text):
    if tts._inLoop:
        tts.endLoop()

    tts.say(text)
    tts.startLoop(False)
    tts.iterate()
    tts.endLoop()

def recognize(audio):
    result1 = r.recognize_faster_whisper(audio, task='translate')
    print(result1)
    if "jarvis" in result1.lower():
        thing = result1.lower().split()
        string = ""
        for i in range(thing.index([i for i in thing if "jarvis" in i][0])+1, len(thing)):
            string = string+" "+thing[i]
        print(string)
        command = string.split(" ")
        command.pop(0)
        print(command)

        if command[0].lower().strip(",.:") == "search":
            query = "+".join(command[1:])
            browse.open(f"https://www.google.com/search?q={query}")
            speak("ok")

        if command[0].lower().strip(".,:") == "help":
            os.system(f"ollama run voiceassistant {' '.join(command)} > cache")
            with open("cache", "r") as file:
                pyautogui.write(file.read())

        else:
            os.system(f"ollama run voiceassistant {' '.join(command)} > cache")
            with open("cache", "r") as file:
                speak(file.read())

    return

r = sr.Recognizer()
while 1:
    with sr.Microphone() as source:
        print("START")
        audio = r.listen(source)
        thread = Thread(target=recognize, args=(audio,)).start()
