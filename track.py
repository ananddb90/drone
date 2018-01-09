#!/usr/bin/env python

import numpy as np
import cv2
import pdb
import sys
import argparse


def upscale():
    """ Upscale the ROI to original size of frame """

def run_main(trackid, fileid):
    """
    (1) Main function to read video and ROIs from user
    (2) Different available tracker in Opencv can be used for further tracking
    """
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[trackid]

    print minor_ver
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
 
    # Read video
    video_files = ['IMG_1743', 'IMG_9223','IMG_9229']
    video = cv2.VideoCapture("AnandVideos/"+video_files[fileid]+".MOV")
 
    # Exit if video not opened.
    if not video.isOpened():
        print "Could not open video"
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print 'Cannot read video file'
        sys.exit()
     
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)
 
    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)

    # crop ROI from an image
    imCrop = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
 
    pdb.set_trace()
    #cv2.imshow("Image",imCrop)
    #cv2.waitKey(0)
    #height, width = img.shape[:2]
    res = cv2.resize(imCrop,(2*100, 2*100), interpolation = cv2.INTER_CUBIC)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='demo')
    parser.add_argument('--tracker', dest='trackid', help='name of tracker to be used',
                        default=1, type=int)
    parser.add_argument('--file', dest='fileid', help='name of video file without extension',
                        default=1, type=int)

    args = parser.parse_args()

    return args

 
if __name__ == '__main__' :
    """
    Read user arguemnt to select video file and tracker type
    """
    args = parse_args()
    pdb.set_trace()
    run_main(args.trackid, args.fileid)

