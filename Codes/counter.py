## counter
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
from Bee import Bee
from Utils import Utils

EntranceCounter = 0
ExitCounter = 0
coorYCrossingline = 540
camera = cv2.VideoCapture('video_name')

def checkentrance(bee, coorYCrossingline):
    if bee.positionY<coorYCrossingline and bee.historyPosition[len(historyPosition)-1][1]>coorYCrossingline:
        return True
    else:
       return False

def checkexit(bee, coorYCrossingline):
    if bee.positionY>coorYCrossingline and bee.historyPosition[len(historyPosition)-1][1]<coorYCrossingline:
        return True
    else:
        return False
while True:
    (grabbed, frame) = camera.read()
    for bee in beeTable:
        if checkentrance == True:
            EntranceCounter = EntranceCounter + 1
        if checkexit == True:
            ExitCounter = ExitCounter + 1
    cv2.putText(frame, "Entrances: {}".format(str(EntranceCounter)), (10, 50),
                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(frame, "Exits: {}".format(str(ExitCounter)), (10, 70),
                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
