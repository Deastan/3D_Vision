import numpy as np
import cv2

#Don t forget to change the name of the video
cap = cv2.VideoCapture('GOPR1292.MP4')

#MOG3
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
#fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

#MOG2
#fgbg = cv2.createBackgroundSubtractorMOG2()
#MOG
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()