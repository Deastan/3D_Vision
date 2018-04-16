from Bee import Bee
from Utilities import Utilities
import numpy as np
import cv2
import time

# ************************************************************
# Define the goal of the program, paths of the video
# ************************************************************

# Do you want to calculate the distorsion of the camera ? true = yes and false = no
calculateDistorsion = False
calculateDistorsionPath =  '/home/jonathan/git/3D_Vision/JohnVideos/calibration_easter_hive'
# Do you want to calibrate the movie ? true = yes and false = no
calibrateVideo = False
# Define the path of the video that you want to use !
videoPath =  '/home/jonathan/Desktop/Videos/GOPR1355FPS60.MP4'
# Do you want to track the bees ? It's funy. Do it !
tracking = True


# ************************************************************
#
# Attention !    To the user :
#                Don't change anything below
#
# ************************************************************

# Calculate distortion
if calculateDistorsion == True:
    print("The measure of the distortion is set!")
    Utilities.calculateDistorsion(path = calculateDistorsionPath)
else:
    print("The measure of the distortion is not set!")

# Calibrate the video
if calibrateVideo == True:
    print("The calibration of the video is set!")
    Utilities.calibrateVideo(path = videoPath)
else:
    print("The calibration of the video is not set!")

# Traking bee
if tracking == True:
    print("Part of Philip is set")
    Utilities.trackingPhilipp(path = videoPath)
else:
    print("Part of Philip  is not set!")

