from matplotlib import pyplot as plt
import numpy as np
import cv2

cap = cv2.VideoCapture('GOPR1352120FPS.MP4')
ret,frame = cap.read()
fgbg = cv2.createBackgroundSubtractorMOG2()


# define field of interst
higth1 = 450
higth2 = 600
width1 = 500
width2 = 600
higth = higth2-higth1
width = width2-width1


fourcc = cv2.VideoWriter_fourcc(*'DIVX')
print(frame.shape)
out = cv2.VideoWriter('output.avi',fourcc,20.0,(higth,width),True)

while(1):
    ret, frame = cap.read()
    if ret == False:
        break
    frame = frame[higth1:higth2,width1:width2,:]
    fgmask = fgbg.apply(frame)
    ret, thresh = cv2.threshold(fgmask,127,255,0)
    median = cv2.medianBlur(thresh,9)
    inv = cv2.bitwise_and(frame,frame, mask=median)

    out.write(frame)

    cv2.imshow('frame',frame)
    cv2.imshow('median',median)
    cv2.imshow('inv',inv)
    k=cv2.waitKey(1) & 0xFF
    if k ==27:
        break

cap.release()
out.release()
