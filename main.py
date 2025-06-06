import speech_recognition as sr
import pyttsx3 as ts

tts = ts.init()
tts.setProperty('rate', 170)

r = sr.Recognizer()
while 1:
    with sr.Microphone() as source:
        audio = r.listen(source)
        result1 = r.recognize_faster_whisper(audio)
        print(result1)
        if "jarvis" in result1.lower():
            thing = result1.lower().split()
            string = ""
            for i in range(thing.index([i for i in thing if "jarvis" in i][0])+1, len(thing)):
                string = string+" "+thing[i]
            tts.say(string)
            tts.runAndWait()
