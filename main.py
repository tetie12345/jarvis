import threading
from time import sleep
import speech_recognition as sr
import pyttsx3 as ts
import webbrowser as browse
from threading import Thread
import os
import pyautogui
from pycmus import remote
from rapidfuzz import fuzz, process, utils

tts = ts.init()
tts.setProperty("rate", 170)
try:
    player = remote.PyCmus()
    cmusIsRunning = True
except Exception:
    print("cmus player is not running, music functionality disabled")
    cmusIsRunning = False

playingSongs = []


def speak(text):
    if tts._inLoop:
        tts.endLoop()

    tts.say(text)
    tts.startLoop(False)
    tts.iterate()
    tts.endLoop()


def stopSpeaking():  # Doesn't work yet
    tts.stop()
    tts.endLoop()


def stopSong():
    global player
    player.player_stop()

    speak("ok")


def recognize(audio):
    print(f"started recognizing on new thread {threading.current_thread().ident}")
    result1 = r.recognize_faster_whisper(audio, compute_type="float32", model="base")
    print(result1)
    if "jarvis" in result1.lower():
        thing = result1.lower().split()
        string = ""
        for i in range(
            thing.index([i for i in thing if "jarvis" in i][0]) + 1, len(thing)
        ):
            string = string + " " + thing[i]
        print(string)
        command = string.split(" ")
        command.pop(0)
        print(command)

        if command[0].lower().strip(",.:") == "search":
            query = "+".join(command[1:])
            browse.open(f"https://www.google.com/search?q={query}")
            speak("ok")

        elif command[0].lower().strip(".,:") in ["help", "helped", "write", "right"]:
            os.system(f"ollama run llama3.2:3b {' '.join(command)} > cache")
            with open("cache", "r") as file:
                pyautogui.write(file.read(), interval=0)

        elif command[0].lower().strip(",.:") == "stop":
            stopSong()

        elif command[0].lower().strip(".,:") == "repeat":
            with open("cache", "r") as file:
                speak(file.read())

        elif command[0].lower().strip(",.:") in [
            "play",
            "played",
            "player",
            "plain",
            "playing",
            "plays",
        ]:
            if len(command) == 1:
                player.player_play()
                speak("ok")
                return
            query = " ".join(command[1:])
            os.system("find ~/music > cache")
            with open("cache", "r") as file:
                songs = [i.removesuffix("\n") for i in file.readlines()]

            songs = process.extract(
                query=query,
                choices=songs,
                scorer=fuzz.partial_token_sort_ratio,
                processor=utils.default_process,
                score_cutoff=35,
            )

            print(songs)
            song = songs[0][0]

            if os.path.isfile(song):
                speak(
                    f"now playing {os.path.basename(song).split("-")[1].removesuffix('.mp3')} by {os.path.basename(song).split("-")[0]}"
                )
            sleep(2)
            player.player_play_file(song)

        elif command[0].lower().strip(".,:") in ["pause", "paws", "paused"]:
            player.player_pause()
            speak("ok")

        elif command[0].lower().strip(",.;") == "skip":
            player.player_next()
            speak("ok")

        else:
            os.system(f"ollama run voiceassistantV2 {' '.join(command)} > cache")
            with open("cache", "r") as file:
                speak(file.read())

    return


r = sr.Recognizer()
while 1:
    with sr.Microphone() as source:
        print("START")
        audio = r.listen(source)
        thread = Thread(target=recognize, args=(audio,), daemon=True).start()
