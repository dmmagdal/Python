# faceRec.py
# Simple facial detection program. Should pick out faces from the
# user's camera and highlight the eyes as well.
# https://www.geeksforgeeks.org/opencv-python-program-face-detection/
# Python 3.6
# Linux

import cv2


# Load the required xml classifiers.
# https://github.com/Itseez/opencv/blob/master/
# data/haarcascades/haarcascade_frontalface_default.xml
# Trained XML classifiers describes some features of some object we
# want to detect. A cascade function is trained from a lot of positive
# (faces) and nectaive (non-faces) images.
# Note: These paths must be for the xml files. 
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

# https://github.com/Itseez/opencv/blob/master
# /data/haarcascades/haarcascade_eye.xml
# Trained XML file for detecting eyes.
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

# Capture frames from camera
cap = cv2.VideoCapture(0)

# Loop continuously runs if capturing has been initialized.
while True:
	# Read frames from camera.
	ret, img = cap.read()

	# Convert to gray scale each of the frames.
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Detect faces of different sizes in the input image.
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
		# Draw a rectangle around a face.
		cv2.rectangle(img, (x,y), (x+w,y+h), (255, 255, 0), 2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]

		# Detect eyes of different sizes in the input image.
		eyes = eye_cascade.detectMultiScale(roi_gray)

		# Draw rectangles around the eyes.
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0, 255, 255), 2)

	# Display an image in a window.
	cv2.imshow('img', img)

	# Wait for the Esc key to stop.
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

# Close the window.
cap.release()

# Deallocate any associated memory usage.
cv2.destroyAllWindows()