import cv2
import numpy as np
import os
from Bee import Bee
import sys

class Utils:

    @staticmethod
    def getPosBee(videoPath):
        ### This method returns the ROI of the Bees (a, b, c, d)###
        cap = cv2.VideoCapture(videoPath)
        fgbg = cv2.createBackgroundSubtractorMOG2()
        a = []
        b = []
        c = []
        d = []
        while(a==[]):
            ret, frame = cap.read()
            fgmask = fgbg.apply(frame)
            ret, thresh = cv2.threshold(fgmask,127,255,0)
            median = cv2.medianBlur(thresh,5)
            blur = cv2.GaussianBlur(median,(5,5),0)
            img,contours, hierarchy = cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            if contours !=[]:
                newContours = contours
                for cnt in contours:
                    A = cv2.contourArea(cnt)
                    if (A>500):
                        M = cv2.moments(cnt)
                        cx = (M["m10"]/M["m00"])
                        cy = (M["m01"]/M["m00"])
                        n = np.sqrt(A/2)
                        a.append(cx)
                        b.append(cy)
                        c.append(2*n)
                        d.append(n)
        # print(frame.shape)
        # print(a,b,c,d)
        return a,b,c,d



    @staticmethod
    def updateBee(cx,cy,bee, beenr):
        bee.counter=0
        bee.id = beenr
        print('beenr')
        bee.update = True
        bee.state = 2
        bee.speedX = bee.positionX-cx
        bee.speedY = bee.positionY-cy
        bee.PositionX = cx
        bee.PositionY = cy
        return bee

    @staticmethod
    def drawBee(bee, frame):
        ellipse = cv2.fitEllipse(bee.cnt)
        cv2.ellipse(frame,ellipse,(0,0,255),2)
        # bee.screen()
        cv2.putText(frame,str(bee.id),(int(bee.positionX),int(bee.positionY)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
        return frame


    @staticmethod
    def checkDist(cx,cy, beeTable):
        # print(beeTable)
        incr = True
        beenr = 0
        # print(beeTable)
        r =  []
        for i in beeTable:
            if i.state ==2:
                dx = (cx-i.speedX) -i.positionX
                dy = (cy-i.speedY) -i.positionY
            elif (i.state==3):
                dx = (cx-i.speedX*i.counter)-i.positionX
                dy = (cy-i.speedY*i.counter)-i.positionY
            # test if it could be the same be, because of its relative position towards other bees
            else:
                dx = cx-i.positionX
                dy = cy-i.positionY
            r.append(np.sqrt(pow(dx,2)+pow(dy,2)))
            # print(r)

            # check with looking at the speed
        if beeTable:
            rmin = np.amin(r)
            if(rmin <150): # if it is without prediction of position use rmin < 150

                # print('rmin: ', rmin)
                # print('r: ', r)
                bee = beeTable[np.argmin(r)]
                if bee.counter<10:
                    # print('found Bee')
                    beenr = np.argmin(r)
                    # print(beenr)
                    incr = False
        return (incr, beenr)
