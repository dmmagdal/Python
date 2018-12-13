# imgops.py
# taken from https://pythonprogramming.net/loading-images-python-opencv-tutorial/
# Python 3.6
# Linux

import cv2
import numpy as np


def main():
	img = cv2.imread("watch.jpg", cv2.IMREAD_COLOR)

	# Reference specific pixels.
	px = img[55,55]
	# Change the pixel.
	img[55,55] = [255,0,0]
	# Then rereference.
	px = img[55,55]
	print(px)

	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()
