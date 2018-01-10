#!/usr/bin/python

#-------------------------------------------------------------------------------------------------------
# https://stackoverflow.com/questions/28308057/motion-detector-for-moving-camera-on-opencv
#
# In order to be able to differentiate between camera motion and scene motion, you need to simultaneously estimate the pose change of the camera # between two frames and the scene geometry in those frames.
#
# There are methods that accomplish this, you should look into structure from motion (SfM), and fundamental matrix estimation. These are
# complicated methods, and each comes with its own issues (e.g. in case of small translations, the estimation of scene depth may be inaccurate).
# However, you need this kind of method since your moving objects only distinguish themselves from the scene when you look at their motion in
# world coordinates, instead of image coordinates.


#-------------------------------------------------------------------------------------------------------

import cv2
import sys
import numpy as np
 
if len(sys.argv) < 2:
    video_capture = cv2.VideoCapture(0)
else:
    video_capture = cv2.VideoCapture(sys.argv[1])


# Read two frames, last and current, and convert current to gray.
ret, last2last_frame = video_capture.read()
ret, last_frame = video_capture.read()
ret, current_frame = video_capture.read()
gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)



def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()


i = 0
while(True):
    # We want two frames- last and current, so that we can calculate the different between them.
    # Store the current frame as last_frame, and then read a new one
    last2last_frame = last_frame
    last_frame = current_frame

    ret, current_frame = video_capture.read()
    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Find the absolute difference between frames
    diff = cv2.absdiff(last_frame, current_frame)
    diff2 = cv2.absdiff(last2last_frame, last_frame)
    motion_detection_frame = cv2.bitwise_and(diff, diff2)
    #motion_detection_frame = cv2.bitwise_xor(diff, diff2)
    # If difference is greater than a threshold, that means motion detected.
    if np.mean(motion_detection_frame) > 5:
        print("Motion detected.")

    text = "Not Blurry"
    fm = variance_of_laplacian(motion_detection_frame)
    if variance_of_laplacian(motion_detection_frame) < 100:
	text = "Blurry"

    # Display the resulting frame
    cv2.imshow('Video',motion_detection_frame)
    cv2.putText(motion_detection_frame, "{}: {:.2f}".format(text, fm), (10, 30),
		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
    	break

    # When everything done, release the capture
video_capture.release()
cv2.destroyAllWindows()



