from Utilities_2 import Utilities_2
import numpy as np
import cv2
import os

# ************************************************************
# Define the goal of the program, paths of the video
# ************************************************************

# Do you want to calculate the distorsion of the camera ? True = yes and False = no
calculateDistorsion = False

# Do you want to calibrate the movie ? True = yes and False = no
calibrateVideo = False

# Define the path of the video that you want to use ! For example:
videoPath = '/home/philipp/Desktop/GOPR1402.MP4'

# Do you want to track the bees ? It's funny. Do it !
tracking = True

# ************************************************************
# ************************************************************


# Calculate distortion
if calculateDistorsion == True:
    print("The measure of the distortion is set!")
    Utilities_2.calculateDistorsion()
else:
    print("The measure of the distortion is not set!")

# Calibrate the video
if calibrateVideo == True:
    print("The calibration of the video is set!")
    Utilities_2.calibrateVideo(path = os.path.join(videoPath))
else:
    print("The calibration of the video is not set!")

# Tracking bees
if tracking == True:
    print("Tracking is set")
    Utilities_2.trackingPhilipp(path = videoPath, videoWrite=True) #set videoWrite on 'True' if you want to save the displayed video
else:
    print("Tracking is not set!")

