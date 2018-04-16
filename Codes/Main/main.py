from Bee import Bee
from Utilities import Utilities
import numpy as np
import cv2
import time
import os

# ************************************************************
# Define the goal of the program, paths of the video
# ************************************************************

# Do you want to calculate the distorsion of the camera ? True = yes and False = no
calculateDistorsion = False

# Do you want to calibrate the movie ? True = yes and False = no
calibrateVideo = True

# Define the path of the video that you want to use ! For example: GOPR1355FPS60.MP4
videoName = 'GOPR1345.MP4'

# videoPath =  '/home/jonathan/Desktop/Videos/'

# Do you want to track the bees ? It's funy. Do it !
tracking = True

# ************************************************************
#
# Attention !    To the user :
#                Don't change anything below
#
# ************************************************************

# Define paths:
currentPath = os.getcwd()
videoPath = os.path.join('../../Media',videoName)

# Calculate distortion
if calculateDistorsion == True:
    print("The measure of the distortion is set!")
    Utilities.calculateDistorsion()
else:
    print("The measure of the distortion is not set!")

# Calibrate the video
if calibrateVideo == True:
    print("The calibration of the video is set!")
    Utilities.calibrateVideo(path = os.path.join(currentPath,videoPath))
else:
    print("The calibration of the video is not set!")

# Traking bee
if tracking == True:
    print("Part of Philipp is set")
    Utilities.trackingPhilipp(path = os.path.join(currentPath,videoPath))
else:
    print("Part of Philipp is not set!")
