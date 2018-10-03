# wait2.py
# Cycles every 10 seconds. Waits for a queue with speech recognition.
# Python 3.6
# Windows 10

import speech_recognition as sr
from threading import Thread
import time

def listen(r, audio):
	vRecogEng = "Google"
	#vRecogEng = "Sphinx"

	print("Listening")

	'''
	# Listen for commands.
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		#print("say something")
		audio = r.listen(source)
	'''

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
		except:
			print("This is an error")


def main():
	# while True:
	r = sr.Recognizer()
	m = sr.Microphone()
	with m as source:
		r.adjust_for_ambient_noise(source)

	print("foo")

	# stop_listening = r.listen_in_background(m, listen)
	t = Thread(target=r.listen_in_background, args=(m, listen))
	t.start()

	# for _ in range(50):
	# 	time.sleep(0.1)
	time.sleep(5)

	t.join()

	print("baz")





if __name__ == '__main__':
	main()