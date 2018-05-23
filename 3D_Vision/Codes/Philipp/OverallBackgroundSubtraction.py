import numpy as np
import cv2

average = cv2.imread('/home/philipp/Desktop/average.jpg', 1)

#1=color, 0=gray, -1 = no change
cap = cv2.VideoCapture('/home/philipp/Desktop/GOPR1345.MP4')

while(cap.isOpened()):
    ret, frame = cap.read()
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    average=cv2.cvtColor(average, cv2.COLOR_BGR2HSV)
    frame = (average-frame)
    frame[:,:,0:2]=0
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, frame = cv2.threshold(frame,150,255, cv2.THRESH_BINARY) #important to put ret!
    frame=cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

    kernel = np.ones((1,1),np.uint8)
    erosion = cv2.erode(frame,kernel,iterations = 1)
    dilation = cv2.dilate(frame,kernel,iterations = 1)
    frame = np.vstack((frame, erosion))

    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', 1200,800)
    cv2.imshow('frame',frame)
    if cv2.waitKey(30) & 0xFF == ord('q'): #Change frame-speed; close when q is pressed
        break

cap.release()
cv2.destroyAllWindows()
