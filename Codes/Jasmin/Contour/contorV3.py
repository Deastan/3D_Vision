import numpy as np
import cv2
import os
from Bee import Bee
from Utils import Utils




videoName = 'GOPR1402.MP4'
currentPath = os.getcwd()
videoPath = os.path.join('../../../Media',videoName)


cap = cv2.VideoCapture(videoPath)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('tracking_test.avi',fourcc,20.0,(1920,1080))

# fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold = 100)

fgbg = cv2.createBackgroundSubtractorMOG2() #, varThreshold = 50)

beeTable = []
i = 0
ellipsefit = False
incr = True
newBeeTable = []
testBeeTable = []
BeenrInit = True
maxcounter = 5
anzBees = 0
beenrUpdate = False

while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    ret, thresh = cv2.threshold(fgmask,127,255,0)
    median = cv2.medianBlur(thresh,5)
    # plt.subplot(121),plt.imshow(frame),plt.title('Original')
    # plt.subplot(122),plt.imshow(median),plt.title('median')
    blur = cv2.GaussianBlur(median,(5,5),0)
    # print(blur.shape)
    lostBeesTable=[]

    img,contours, hierarchy = cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if contours !=[]:
        anzBees = len(beeTable)
        newBeeTable = []
        for cnt in contours:
            if (cv2.contourArea(cnt)>500):
                M = cv2.moments(cnt)
                cx = (M["m10"]/M["m00"])
                cy = (M["m01"]/M["m00"])
                if BeenrInit:
                    beeTable.append(Bee(len(beeTable),int(cx),int(cy),0,0,0,0,True,cnt))
                    beenrUpdate=True
                    # print(len(beeTable))
                else:
                    newBeeTable.append(Bee(len(newBeeTable)+len(beeTable),int(cx),int(cy),0,0,0,0,True,cnt))
        if beenrUpdate:
            BeenrInit=False

        for bee in beeTable:
            cx = bee.positionX
            cy = bee.positionY
            # bee.screen()
            # Check if bee is in the new table
            lost, beenr = Utils.checkDist(cx,cy, newBeeTable)
            if lost:
                # check if bee is in lost bees
                lostagain, beenr = Utils.checkDist(cx,cy,lostBeesTable)
                if lostagain:
                    # check if the new bee should be added to the beeTable
                    bee.state = 3
                    lostBeesTable.append(bee)
                else:
                    bee = Utils.updateBee(cx,cy,bee,bee.id)
                    beeTable[beenr] = bee
                    ellipse = cv2.fitEllipse(bee.cnt)
                    cv2.ellipse(frame,ellipse,(0,0,255),2)
                    cv2.putText(frame,str(bee.id),(int(bee.positionX),int(bee.positionY)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
                    # frame = Utils.drawBee(bee,frame)
            else:
                bee = Utils.updateBee(cx,cy,bee,bee.id)
                beeTable[beenr] = bee
                frame = Utils.drawBee(bee,frame)
                ellipse = cv2.fitEllipse(bee.cnt)
                cv2.ellipse(frame,ellipse,(0,0,255),2)
                cv2.putText(frame,str(bee.id),(int(bee.positionX),int(bee.positionY)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)


        # cv2.imshow('newContours',frame)
        for bee in lostBeesTable:
            if((cx<1920/25*3)|(cy>1080/18*2)|(cx>1920/25*22)):
                beeTable.append(bee)
            bee.counter +=1
        for bee in beeTable:
            if bee.update:
                frame = Utils.drawBee(bee,frame)
                # bee.update = False

        cv2.imshow('newContours',frame)
        out.write(frame)
        k=cv2.waitKey(30) & 0xFF
        if k ==27:
            break
cap.release()
out.release()
cv2.destroyAllWindows()

# try the algorithm which is in the video, migth this be the migthy
