import cv2
import numpy as np
import os
from Bee import Bee
import sys

class Utils:

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
            elif i.state==3:
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
                    beenr = np.argmin(r)
                    # print(beenr)
                    incr = False
        return (incr, beenr)
