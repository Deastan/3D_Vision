import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture('GOPR1353.MP4')
fgbg = cv2.createBackgroundSubtractorMOG2(history = 10000000) #, varThreshold = 50)

while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    ret, thresh = cv2.threshold(fgmask,127,255,0)
    median = cv2.medianBlur(thresh,9)
    blur = cv2.GaussianBlur(median,(9,9),0)

    # show the different videos
    cv2.imshow('median',median)
    cv2.imshow('original',frame)
    cv2.imshow('thresh',thresh)
    cv2.imshow('blur',blur)

    # implement function to find contours
    img,contours, hierarchy = cv2.findContours(blur,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if contours !=[]:

        for cnt in contours:
            # area = cv2.contourArea(cnt)

            # do ellipse fitting
            ellipse = cv2.fitEllipse(cnt)
            cv2.ellipse(frame,ellipse,(0,0,255),2)

        cv2.imshow('contours',frame)

    k=cv2.waitKey(1) & 0xFF
    if k ==27:
        break
cap.release()
cv2.destroyAllWindows()

