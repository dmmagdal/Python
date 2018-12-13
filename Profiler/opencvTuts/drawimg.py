# drawimg.py
# taken from https://pythonprogramming.net/loading-images-python-opencv-tutorial/
# Python 3.6
# Linux

import cv2
import numpy as np


def main():
	img = cv2.imread("watch.jpg", cv2.IMREAD_COLOR)

	# Draw a line. 
	# (img, start coord, end coord, color, width).
	cv2.line(img, (0,0), (150,150), (255,0,255), 15)
	# Draw a rectanlge.
	cv2.rectangle(img, (15,15), (200,215), (0,0,255), 15)
	# Draw a circle.
	# Negative thickness means the object is filled in.
	cv2.circle(img, (100,63), 55, (0,255,0), -1)
	# Draw a polygon.
	pts = np.array([[10,5], [20,30], [70,20], [50,10]], np.int32)
	# (img, coordinates, connect starting and final dot?, color, width)
	cv2.polylines(img, [pts], True, (0,255,255), 3)
	# Write on image.
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img, "OpenCV tutorial", (0,130), font, 1, (0,0,0), 2, cv2.LINE_AA)

	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()
