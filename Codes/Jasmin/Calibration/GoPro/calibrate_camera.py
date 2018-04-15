# This code plays a distorted video with the distortion parameters calculated from another video with the size 1920x1080

import numpy as np
import cv2
import glob

# Load the calibration parameters
ret = np.load('ret.npy')
mtx = np.load('mtx.npy')
dist = np.load('dist.npy')
rvecs = np.load('rvecs.npy')
tvecs = np.load('tvecs.npy')

# Load the video
cap = cv2.VideoCapture('GOPR1352120FPS.MP4') # Place the name of the video you want to play

while(1):
    ret, frame = cap.read()

    frame = cv2.resize(frame,(1920,1080),interpolation=cv2.INTER_LINEAR) # Adapt the imagesize
    h,  w = frame.shape[:2]

    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)

    # show both videos the original called 'frame' and the undistorted called 'dist'
    cv2.imshow('frame',frame)
    cv2.imshow('dist',dst)
    k = cv2.waitKey(1)&0xFF
    if k ==27:
        break

cap.release()
cv2.destroyAllWindows()

