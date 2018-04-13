import numpy as np
import cv2

average = cv2.imread('/home/philipp/Desktop/average.jpg', 1)

#1=color, 0=gray, -1 = no change
cap = cv2.VideoCapture('/home/philipp/Desktop/GOPR1345.MP4')

while(cap.isOpened()):
    ret, frame = cap.read()
    frame = average-frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # ret, frame = cv2.threshold(frame,150,255, cv2.THRESH_BINARY) #important to put ret!

    cv2.imshow('windowName', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'): #Change frame-speed; close when q is pressed
        break

cap.release()
cv2.destroyAllWindows()
