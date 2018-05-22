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
var = False
lost = 5
anzBees = 0

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
                    beeTable.append(Bee(len(beeTable),int(cx),int(cy),0,0,0,0),True)
                    # beeTableOld = beeTable
                else:
                    newBeeTable = append(Bee(len(newBeeTable),int(cx),int(cy),0,0,0,0,True))

        BeenrInit=False

        for bee in beeTable:
            cx = bee.positionX
            cy = bee.positionY
            # Check if bee is in the new table
            lost, beenr = Utils.checkDist(cx,cy, newBeeTable)
            if lost:
                # check if bee is in lost bees
                lostagain, beenr = Utils.checkDist(cx,cy,lostBeesTable)
                if lostagain:
                    bee.counter+=1
                    lostBeesTable.append(bee)
                    bee.state = 3

                else:
                    bee.counter=0
                    bee.id = beenr
                    bee.update = True
                    bee.state = 2
                    #missing the update of the bee!!
            else:
                # bee.counter = 0
                bee.id = beenr
                bee.update = True
                bee.state = 2



                    incr, beenr = Utils.checkDist(cx,cy, beeTable)
                    if incr:
                        newBee.id = len(beeTable)


                        beeTable.append(newBee)
                        ellipse = cv2.fitEllipse(cnt)
                        cv2.ellipse(frame, ellipse, (0,0,255),2)
                        cv2.putText(frame,str(newBee.id),(int(cx),int(cy)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)

                    else:
                        currentBee = beeTable[beenr]
                        currentBee.speedX = currentBee.positionX-cx
                        currentBee.speedY = currentBee.positionY-cy
                        currentBee.state = 2
                        currentBee.counter =0
                        currentBee.update = True
                        currentBee.newPosition(int(cx),int(cy))
                        beeTable[beenr]=currentBee
                        currentBee.screen()
                        ellipse = cv2.fitEllipse(cnt)
                        cv2.ellipse(frame, ellipse, (0,0,255),2)
                        print(beenr)
                        cv2.putText(frame,str(beenr),(int(cx),int(cy)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)




            for i in range(0, anzBees):
                bee = beeTable[i]
                if bee.update==False:
                    bee.counter +=1
                    if bee.state != 3:
                        bee.state =3

            BeenrInit=False
        cv2.imshow('newContours',frame)
        # cv2.imshow('newContours',median)
        out.write(frame)
        k=cv2.waitKey(30) & 0xFF
        if k ==27:
            break
cap.release()
out.release()
cv2.destroyAllWindows()

# try the algorithm which is in the video, migth this be the migthy
