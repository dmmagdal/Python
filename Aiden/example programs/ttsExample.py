# ttsExample.py
# Quick example with the pyttsx3 engine.

import pyttsx3

engine = pyttsx3.init()
engine.say("hello there")
engine.runAndWait()