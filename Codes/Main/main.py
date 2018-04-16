from Bee import Bee
from Utilities import Utilities
import numpy as np
import cv2
import time

# ************************************************************
# Define the goal of the program, paths of the video
# ************************************************************

# Do you want to calculate the distorsion of the camera ? true = yes and false = no
calculateDistorsion = True
calculateDistorsionPath =  '/home/jonathan/git/3D_Vision/JohnVideos/calibration_easter_hive'
# Do you want to calibrate the movie ? true = yes and false = no
calibrateVideo = True
# Define the path of the video that you want to use !
videoPath =  '/home/jonathan/Desktop/Videos/GOPR1353FPS60.MP4'



# ************************************************************
# Codes
# ************************************************************

# Calculate distortion
if calculateDistorsion == True:
    print("The measure of the distortion is set!")
    Utilities.calculateDistorsion(path = calculateDistorsionPath)
else:
    print("The measure of the distortion is not set!")

# Calculate distortion
if calculateDistorsion == True:
    print("The calibration of the video is set!")
    Utilities.calibrateVideo(path = videoPath)
else:
    print("The calibration of the video is not set!")



# Code from Philipp

cap = cv2.VideoCapture(videoPath)
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec and create VideoWriter object (fourcc)
init = 0
fgbg = cv2.createBackgroundSubtractorMOG2()
counter = 0
beesTable1 = [] # table which content the bees

while (1):


    ret, original = cap.read()

    # if init == 0:
    #     out = cv2.VideoWriter('/home/philipp/Desktop/video_circle.avi', fourcc, 10, (original.shape[1], original.shape[0]))  # define: format, fps, and frame-size (pixels)
    #     init = 1
    # out.write(original)


    original = Utilities.defineROI(100,1700,500,750,original)

    # create bg-subtracted, thresholded and median-filtered image
    fgmask = fgbg.apply(original)
    fgmask = cv2.medianBlur(fgmask, 9)
    ret, fgmask = cv2.threshold(fgmask, 120, 255, cv2.THRESH_BINARY)
    kernel = np.ones((35, 35), np.uint8)
    # erosion = cv2.erode(fgmask,kernel,iterations = 1)
    # fgmask = cv2.dilate(fgmask, kernel, iterations=1)



    Utilities.connectedComponents(original=original,fgmask=fgmask, connectivity=8, beesTable=beesTable1)

    cv2.putText(original, "frame:" +str(counter+1),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.namedWindow('frame_median', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame_median', 1200, 800)
    cv2.imshow('frame_median', original)



    # labels=labels*50000
    # cv2.imshow('frame_median', labels)
    # if counter==2:
    #     cv2.imwrite('/home/philipp/Desktop/white.jpg',original)
    #     break


#*************************************
# There is an error in these 2 next line
#*************************************
    #counter += 1
    #print("\r frame" + str(counter), end="")

    #
    # # time.sleep(1)
    # if counter==4:
    #     Utilities.getHistogram(original)
    #     break


    k = cv2.waitKey(1) & 0xff  # modify the frame-speed
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
