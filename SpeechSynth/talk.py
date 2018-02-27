# simple program that can verbally echo an input line
import pyttsx3              # import pyttsx3 module (also requires pywin32 module

engine = pyttsx3.init()     # create an engine out of the module
echo = str(input())         # input to be echoed out
engine.say(echo)            # engine says echo
engine.runAndWait()         # end of program
