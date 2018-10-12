# wait3.py
# Cycles every 10 seconds. Waits for a queue with speech recognition.
# Python 3.6
# Windows 10

import speech_recognition as sr
import pyaudio, os
from threading import Thread
import time

'''
def mainFunc(r, source):
    audio = r.listen(source)
    user = r.recognize_google(audio)
    print(user)
    if user != '':
        print (user)


def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            mainFunc(r, source)


if __name__ == '__main__':
    main()
'''

def internet():
    print("Accessing internet")

def music():
    print("Playing music")

def mainfunction(source):
    audio = r.listen(source)
    try:
        user = r.recognize_google(audio)
        print(user)
        if user == "internet":
            internet()
        elif user == "music":
            music()
    except:
        print("listening")
        pass

if __name__ == '__main__':
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            mainfunction(source)