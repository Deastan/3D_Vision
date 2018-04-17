from Codes.Philipp.Utilities import Utilities
import numpy as np
import cv2
import time


cap = cv2.VideoCapture('/home/philipp/Desktop/GOPR1402.MP4')
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec and create VideoWriter object (fourcc)
init = 0
fgbg = cv2.createBackgroundSubtractorMOG2()
counter = 0
beesTable = []
global blueArray
blueArray_static=[0 for x in range(255)]
greenArray_static=[0 for x in range(255)]
redArray_static=[0 for x in range(255)]

blueArray=[0 for x in range(255)]
greenArray=[0 for x in range(255)]
redArray=[0 for x in range(255)]

blueArray_static, greenArray_static, redArray_static = Utilities.defineStaticArrays(blueArray_static, greenArray_static, redArray_static)


def createHistoArray(frame, label):
    global blueArray, greenArray, redArray
    if counter==frame:
        cv2.destroyAllWindows()
        # Utilities.showCaughtPatch(realoriginal, labels, label)
        # cv2.imshow('windowName', realoriginal)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        blueArray, greenArray, redArray = Utilities.getHistogram(realoriginal, label, blueArray, greenArray, redArray, frame=counter)
        # time.sleep(1)




while (1):


    ret, original = cap.read()



    # if init == 0:
    #     out = cv2.VideoWriter('/home/philipp/Desktop/video_circle.avi', fourcc, 10, (original.shape[1], original.shape[0]))  # define: format, fps, and frame-size (pixels)
    #     init = 1
    # out.write(original)


    original = Utilities.defineROI(100,1700,500,750,original)
    realoriginal=np.array(original)

    # create bg-subtracted, thresholded and median-filtered image
    fgmask = fgbg.apply(original)
    fgmask = cv2.medianBlur(fgmask, 9)
    ret, fgmask = cv2.threshold(fgmask, 120, 255, cv2.THRESH_BINARY)
    kernel = np.ones((35, 35), np.uint8)
    # erosion = cv2.erode(fgmask,kernel,iterations = 1)
    # fgmask = cv2.dilate(fgmask, kernel, iterations=1)



    labels=Utilities.connectedComponents(original=original,fgmask=fgmask, connectivity=8)


    cv2.putText(original, "frame:" +str(counter+1),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.namedWindow('frame_median', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame_median', 1200, 800)
    cv2.imshow('frame_median', original)



    # labels=labels*50000
    # cv2.imshow('frame_median', labels)
    # if counter==2:
    #     cv2.imwrite('/home/philipp/Desktop/white.jpg',original)
    #     break



    counter += 1
    print("\r frame" + str(counter), end="")

    ###I'll have to make all the arrays again, cause I might not have taken all the arrays, as the one from frame 4 is out-commented

    # createHistoArray(22,2)
    # if counter==22:
    #     print(np.dot(blueArray, blueArray_static))
    #     break
    # createHistoArray(4,8, realoriginal)
    createHistoArray(6,1)
    createHistoArray(8,1)
    createHistoArray(16,1)
    createHistoArray(22,2)
    if counter ==22:
        time.sleep(1)
        print("blue:\n",blueArray/5)
        print("green:\n", greenArray/5)
        print("red:\n", redArray/5)
        break




    # time.sleep(7)




    k = cv2.waitKey(1) & 0xff  # modify the frame-speed
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()





