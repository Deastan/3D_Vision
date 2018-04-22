from Codes.Philipp.Utilities import Utilities
import numpy as np
import cv2
import time


frameNumber = 0
global realOriginal #is the image without ellipses/numbers
cap = cv2.VideoCapture('/home/philipp/Desktop/GOPR1402.MP4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec and create VideoWriter object (fourcc)
fgbg = cv2.createBackgroundSubtractorMOG2()

arraySearch = True
######################################################################################################


histoBlue_current=[0 for x in range(256)]
histoGreen_current=[0 for x in range(256)]
histoRed_current=[0 for x in range(256)]


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
    # original = Utilities.defineROI(100,1700,500,750,original)
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
        cv2.namedWindow('Bee recognition', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Bee recognition', 1200, 800)
        cv2.imshow('Bee recognition', original)



    if frameNumber == 1:
        out = cv2.VideoWriter('/home/philipp/Desktop/ellipses.avi', fourcc, 15, (original.shape[1], original.shape[0]))  # define: format, fps, and frame-size (pixels)
    out.write(original)
    print("\r frame" + str(frameNumber), end="")
    # time.sleep(8)








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





