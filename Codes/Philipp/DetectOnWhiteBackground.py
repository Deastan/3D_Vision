import numpy as np
from Utilities import Utilities
import cv2
import time
import os


frameNumber = 0
global realOriginal #is the image without ellipses/numbers
# name of the video:
videoName = 'GOPR1404.MP4'
# define path of the video
currentPath = os.getcwd()
videoPath = os.path.join('../../Media',videoName)
cap = cv2.VideoCapture(videoPath)
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec and create VideoWriter object (fourcc)
fgbg = cv2.createBackgroundSubtractorMOG2()

arraySearch = False
######################################################################################################


histoBlue_current=[0 for x in range(256)]
histoGreen_current=[0 for x in range(256)]
histoRed_current=[0 for x in range(256)]
beesLastFrame =[]

sumBeesIn = 0
sumBeesOut= 0

def createHistoArray(frameTolookAt, labelNumber):
    global histoBlue_current, histoGreen_current, histoRed_current
    if frameTolookAt==frameNumber:
        cv2.destroyAllWindows()
        # Utilities.showCaughtPatch(realOriginal, labels, labelNumber)

        histoBlue_current,histoGreen_current, histoRed_current = Utilities.getHistogramForArraySearch(labelNumber,histoBlue_current,histoGreen_current, histoRed_current, realOriginal)


while (1):
    frameNumber +=1

    ret, original = cap.read()
    if ret==False:
        print('File not found')
        break
    realOriginal=np.array(original)
    fgmask = fgbg.apply(original)
    fgmask = cv2.medianBlur(fgmask, 9)
    ret, fgmask = cv2.threshold(fgmask, 120, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)




    if frameNumber!=1:
        labels, beesCurrentFrame=Utilities.connectedComponents(fgmask, original, realOriginal)
        if frameNumber>=2:
            beesIn, beesOut = Utilities.counter(beesCurrentFrame, beesLastFrame, original)
            sumBeesIn+=beesIn
            sumBeesOut+=beesOut
            cv2.putText(original, "In:" +str(beesIn),(50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(original, "Out:" +str(beesOut),(50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(original, "In_total:" +str(sumBeesIn),(50, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(original, "Out_total:" +str(sumBeesOut),(50, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        beesLastFrame = beesCurrentFrame







    # everything concerning showing the window
    if arraySearch==False:
        cv2.putText(original, "frame:" +str(frameNumber),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.namedWindow('Bee recognition', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Bee recognition', 1200, 800)
        cv2.line(original,(0,570),(1920,570),(255,0,0),2)
        cv2.imshow('Bee recognition', original)



    if frameNumber == 1:
        out = cv2.VideoWriter('/home/philipp/Desktop/ellipses.avi', fourcc, 15, (original.shape[1], original.shape[0]))  # define: format, fps, and frame-size (pixels)
    out.write(original)







    #only for static-Array-creation
    #DO NOT TAKE TWO OUT OF THE SAME FRAME!!!
    if arraySearch == True:
        createHistoArray(7,4)
        createHistoArray(9,1)
        createHistoArray(12,2)
        createHistoArray(13,3)
        createHistoArray(15,3)
        createHistoArray(40,1)
        if frameNumber ==40: #put the last frame that was used!
            NumberOfFrames = 6
            histoBlue_current=[x/NumberOfFrames for x in histoBlue_current]#divide by the number of frames!
            histoGreen_current=[x/NumberOfFrames for x in histoGreen_current]
            histoRed_current=[x/NumberOfFrames for x in histoRed_current]

            print("\nblue:\n", histoBlue_current)
            print("green:\n", histoGreen_current)
            print("red:\n", histoRed_current)

            print("!!!!did you not forget to modify the number of bees and the final framenumber???")
            break





    k = cv2.waitKey(1) & 0xff  # modify the frame-speed
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
