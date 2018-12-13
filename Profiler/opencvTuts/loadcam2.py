# loadcam.py
# taken from https://pythonprogramming.net/loading-images-python-opencv-tutorial/
# Python 3.6
# Linux

import cv2
import numpy as np


def main():
	# Return video from primary webcam on computer.
	cap = cv2.VideoCapture(0)
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

	# Create an infinite loop to stream feed from camera.
	while True:
		# ret is a boolean reagarding whether or not there was a return
		# at all, at the frame is each frame that is returned. If there
		# is no frame, there won't be an error, but a None.
		ret, frame = cap.read()
		# gray is the frame converted to gray.
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		out.write(frame)

		cv2.imshow('frame', gray)
		# If we get a keyand that key is 'q', break out of the loop.
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# Release the webcam and close all windows.
	cap.release()
	out.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()
