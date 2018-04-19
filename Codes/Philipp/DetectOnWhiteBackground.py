from Codes.Philipp.Utilities import Utilities
import numpy as np
import cv2
import time

arraySearch = False

global realoriginal
global blueBee_static
global greenBee_static
global redBee_static

global blueShadow_static
global greenShadow_static
global redShadow_static


cap = cv2.VideoCapture('/home/philipp/Desktop/GOPR1402.MP4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec and create VideoWriter object (fourcc)
init = 0
fgbg = cv2.createBackgroundSubtractorMOG2()
counter = 0
beesTable = []


blueShadow_static=[0 for x in range(255)]
greenShadow_static=[0 for x in range(255)]
redShadow_static=[0 for x in range(255)]

blueBee_static=[0 for x in range(255)]
greenBee_static=[0 for x in range(255)]
redBee_static=[0 for x in range(255)]

blueShadow_static, greenShadow_static, redShadow_static, blueBee_static, greenBee_static, redBee_static = Utilities.defineStaticArrays(blueShadow_static, greenShadow_static, redShadow_static, blueBee_static, greenBee_static, redBee_static)

blueArray_current=[0 for x in range(255)]
greenArray_current=[0 for x in range(255)]
redArray_current=[0 for x in range(255)]

def createHistoArray(frameNumber, labelNumber):
    global blueArray_current, greenArray_current, redArray_current
    if counter==frameNumber:
        cv2.destroyAllWindows()
        Utilities.showCaughtPatch(realoriginal, labels, labelNumber)
        cv2.imshow('windowName', realoriginal)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        blueArray_current, greenArray_current, redArray_current = Utilities.getHistogram(realoriginal, labelNumber, blueArray_current, greenArray_current, redArray_current, counter, realoriginal)
        # time.sleep(1)




while (1):
    counter +=1

    ret, original = cap.read()



    original = Utilities.defineROI(100,1700,500,750,original)
    realoriginal=np.array(original)
    # create bg-subtracted, thresholded and median-filtered image
    fgmask = fgbg.apply(original)
    fgmask = cv2.medianBlur(fgmask, 9)
    ret, fgmask = cv2.threshold(fgmask, 120, 255, cv2.THRESH_BINARY)
    kernel = np.ones((35, 35), np.uint8)
    # erosion = cv2.erode(fgmask,kernel,iterations = 1)
    # fgmask = cv2.dilate(fgmask, kernel, iterations=1)



    labels=Utilities.connectedComponents(fgmask, original, 8, blueShadow_static, greenShadow_static, redShadow_static, blueBee_static, greenBee_static, redBee_static, counter, realoriginal)

    #everything concerning the show-window
    # if arraySearch==False:
        # cv2.putText(original, "frame:" +str(counter),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        # cv2.namedWindow('frame_median', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('frame_median', 1200, 800)
        # cv2.imshow('frame_median', original)

    if init == 0:
        out = cv2.VideoWriter('/home/philipp/Desktop/ellipses_without_histo.avi', fourcc, 15, (original.shape[1], original.shape[0]))  # define: format, fps, and frame-size (pixels)
        init = 1
    out.write(original)



    # labels=labels*50000
    # cv2.imshow('frame_median', labels)
    # if counter==2:
    #     cv2.imwrite('/home/philipp/Desktop/white.jpg',original)
    #     break



    print("\r frame" + str(counter), end="")

    if arraySearch == True:
        createHistoArray(4,2)
        createHistoArray(5,1)
        createHistoArray(6,3)
        createHistoArray(7,4)
        createHistoArray(10,2)
        createHistoArray(21,7)
        # createHistoArray(22,2)
        # createHistoArray(22,2)
        # createHistoArray(22,2)
        # createHistoArray(22,2)
        # createHistoArray(22,2)
        # createHistoArray(22,2)
        # createHistoArray(22,2)
        # createHistoArray(22,2)

        if counter ==21: #put the last frame that was used!
            blueArray_current/=6#divide by the number of frames!
            greenArray_current/=6
            redArray_current/=6

            print("\nblue:\n", blueArray_current)
            print("green:\n", greenArray_current)
            print("red:\n", redArray_current)
            break




    time.sleep(0.05)


    k = cv2.waitKey(1) & 0xff  # modify the frame-speed
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()





