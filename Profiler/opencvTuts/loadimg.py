# loadimg.py
# taken from https://pythonprogramming.net/loading-images-python-opencv-tutorial/
# Python 3.6
# Linux

import cv2
import numpy as np
from matplotlib import pyplot as plt


def main():
	# Load image with applied "filter". Default is cv2.IMREAD_COLOR.
	img = cv2.imread('watch.jpg', cv2.IMREAD_GRAYSCALE)
	# Display.
	cv2.imshow('image', img)
	# Key to close window.
	cv2.waitKey(0)
	# Close windows.
	cv2.destroyAllWindows()
	# Write changes to file.
	cv2.imwrite("watchgrey.jpg", img)


if __name__ == '__main__':
	main()
