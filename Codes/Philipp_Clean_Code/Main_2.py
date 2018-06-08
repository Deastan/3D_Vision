import numpy as np
from Utilities import Utilities
import cv2
import os


###################################################################################################¼###
# Initializations:

frameNumber = 0
global realOriginal #is the image without ellipses/numbers

#define the video-path
videoPath = '/home/philipp/Desktop/GOPR1402.MP4'
#define the path for saving the output-video
outputPath = '/home/philipp/Desktop/BeeCounting_2.avi'

cap = cv2.VideoCapture(videoPath)
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec and create VideoWriter object (fourcc)
fgbg = cv2.createBackgroundSubtractorMOG2(1, 10)

lineHistory =[]

histoBlue_current=[0 for x in range(256)]
histoGreen_current=[0 for x in range(256)]
histoRed_current=[0 for x in range(256)]
beesLastFrame =[]

sumBeesIn = 0
sumBeesOut= 0
######################################################################################################





while (1):
    frameNumber +=1

    ret, original = cap.read()
    if ret==False:
        print('File not found')
        break



    #Background-Subtraction and filtering on the image
    realOriginal=np.array(original)
    fgmask = fgbg.apply(original)
    fgmask = cv2.medianBlur(fgmask, 9)
    ret, fgmask = cv2.threshold(fgmask, 120, 255, cv2.THRESH_BINARY)
    # kernel = np.ones((10, 10), np.uint8)
    # fgmask = cv2.dilate(fgmask, kernel, iterations=1)
    # kernel = np.ones((15, 15), np.uint8)
    # fgmask = cv2.erode(fgmask, kernel, iterations=1)




    if frameNumber == 1:
        out = cv2.VideoWriter(outputPath, fourcc, 4, (original.shape[1], original.shape[0]))  # define: format, fps, and frame-size (pixels)
    else:
        labels, beesCurrentFrame=Utilities.connectedComponents(fgmask, original, realOriginal)
        if frameNumber>=2:
            beesIn, beesOut = Utilities.counter(beesCurrentFrame, beesLastFrame, original, lineHistory)
            sumBeesIn+=beesIn
            sumBeesOut+=beesOut
            cv2.putText(original, "In_total:" +str(sumBeesIn),(50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(original, "Out_total:" +str(sumBeesOut),(50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        beesLastFrame = beesCurrentFrame





    # everything concerning showing the window
    cv2.putText(original, "frame:" +str(frameNumber),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.namedWindow('Bee recognition', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Bee recognition', 1200, 800)
    cv2.line(original,(80,570),(1840,570),(255,0,0),5)
    cv2.line(original,(80,1000),(1840,1000),(255,0,0),5)
    cv2.line(original,(80,570),(80,1000),(255,0,0),5)
    cv2.line(original,(1840,570),(1840,1000),(255,0,0),5)

    cv2.imshow('Bee recognition', original)

    out.write(original)








    k = cv2.waitKey(1) & 0xff  # modify the frame-speed
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
