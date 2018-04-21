from Codes.Philipp.Utilities import Utilities
import numpy as np
import cv2
import time


frameNumber = 0
global realOriginal #is the image without ellipses/numbers
cap = cv2.VideoCapture('/home/philipp/Desktop/GOPR1402.MP4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec and create VideoWriter object (fourcc)
fgbg = cv2.createBackgroundSubtractorMOG2()

arraySearch = False
######################################################################################################


def createHistoArray(frameNumber, labelNumber):
    global blueArray_current, greenArray_current, redArray_current
    if frameNumber==frameNumber: #TODO: wtf???
        cv2.destroyAllWindows()
        Utilities.showCaughtPatch(realOriginal, labels, labelNumber)

        blueArray_current, greenArray_current, redArray_current = Utilities.getHistogram(labelNumber, realOriginal)



while (1):
    frameNumber +=1

    ret, original = cap.read()
    original = Utilities.defineROI(100,1700,500,750,original)
    realOriginal=np.array(original)
    fgmask = fgbg.apply(original)
    fgmask = cv2.medianBlur(fgmask, 9)
    ret, fgmask = cv2.threshold(fgmask, 120, 255, cv2.THRESH_BINARY)
    # kernel = np.ones((35, 35), np.uint8)
    # fgmask = cv2.dilate(fgmask, kernel, iterations=1)




    if frameNumber!=1:
        labels=Utilities.connectedComponents(fgmask, original, realOriginal)






    # everything concerning showing the window
    if arraySearch==False:
        cv2.putText(original, "frame:" +str(frameNumber),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.namedWindow('frame_median', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame_median', 1200, 800)
        cv2.imshow('frame_median', original)



    if frameNumber == 1:
        out = cv2.VideoWriter('/home/philipp/Desktop/ellipses_without_histo.avi', fourcc, 15, (original.shape[1], original.shape[0]))  # define: format, fps, and frame-size (pixels)

    out.write(original)
    print("\r frame" + str(frameNumber), end="")
    # time.sleep(8)








    #only for static-Array-creation
    if arraySearch == True:
        createHistoArray(2,6)
        createHistoArray(5,1)
        createHistoArray(6,3)
        createHistoArray(7,4)
        createHistoArray(10,2)
        createHistoArray(21,7)
        if frameNumber ==21: #put the last frame that was used!
            blueArray_current/=6#divide by the number of frames!
            greenArray_current/=6
            redArray_current/=6

            print("\nblue:\n", blueArray_current)
            print("green:\n", greenArray_current)
            print("red:\n", redArray_current)
            break





    k = cv2.waitKey(1) & 0xff  # modify the frame-speed
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()





