import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture('GOPR1345.MP4')

# fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold = 100)

fgbg = cv2.createBackgroundSubtractorMOG2() #, varThreshold = 50)

while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    ret, thresh = cv2.threshold(fgmask,127,255,0)
    median = cv2.medianBlur(thresh,5)
    # plt.subplot(121),plt.imshow(frame),plt.title('Original')
    # plt.subplot(122),plt.imshow(median),plt.title('median')
    blur = cv2.GaussianBlur(median,(5,5),0)
    cv2.imshow('median',median)
    cv2.imshow('original',frame)
    cv2.imshow('thresh',thresh)
    cv2.imshow('blur',blur)
    print('blur: ',np.min(blur))
    print('blurshape: ',blur.shape)
    img,contours, hierarchy = cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if contours !=[]:
        print('contours:', contours)
        # hull = cv2.convexHull(cnt)
        # print('size of hull', hull.shape)
        contours = cv2.drawContours(frame,contours,-1,(0,255,0),3)
        cv2.imshow('contours',contours)
        # cv2.imshow('hull',hull)
    # cv2.imshow('frame',fgmask)
    k=cv2.waitKey(30) & 0xFF
    if k ==27:
        break
cap.release()
cv2.destroyAllWindows()

# try the algorithm which is in the video, migth this be the migthy

