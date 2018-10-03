# wait.py
# Waits for a queue with speech recognition.
# Python 3.6
# Windows 10

import speech_recognition as sr
import time

def listen():
	vRecogEng = "Google"
	#vRecogEng = "Sphinx"

	print("Listening")

	# Listen for commands.
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		#print("say something")
		audio = r.listen(source)

	# Set speech recognition engine.
	if vRecogEng == "Sphinx":
		try:
			print("Sphinx thinks you said " + r.recognize_sphinx(audio))
			return r.recognize_sphinx(audio)
		except sr.UnknownValueError:
			print("Sphinx could not understand audio")
		except sr.RequestError as e:
			print("Sphinx error; {0}".format(e))
	elif vRecogEng == "Google":
		try:
			print("Google speech recognition thinks you said " + r.recognize_google(audio))
			return r.recognize_google(audio)
		except sr.UnknownValueError:
			print("Google speech recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google speech recognition service; {0}".format(e))

	return ""


def main():
	trigger = ""

	while True:
		if listen() != trigger:
			print("Doing something")
		else:
			print("Doing nothing")
		time.sleep(1)

if __name__ == '__main__':
	main()