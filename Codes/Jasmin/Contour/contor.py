import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
from Bee import Bee
from Utils import Utils




videoName = 'GOPR1402.MP4'
currentPath = os.getcwd()
videoPath = os.path.join('../../../Media',videoName)


cap = cv2.VideoCapture(videoPath)

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

while(1):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    ret, thresh = cv2.threshold(fgmask,127,255,0)
    median = cv2.medianBlur(thresh,5)
    # plt.subplot(121),plt.imshow(frame),plt.title('Original')
    # plt.subplot(122),plt.imshow(median),plt.title('median')
    blur = cv2.GaussianBlur(median,(5,5),0)
    # print(blur.shape)

    img,contours, hierarchy = cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if contours !=[]:
        newContours = contours
        # print('contours:', contours)

        for cnt in contours:
            if cv2.contourArea(cnt)>500:
                M = cv2.moments(cnt)
                cx = (M["m10"]/M["m00"])
                cy = (M["m01"]/M["m00"])
                # print('centroid', cx,cy)
                if BeenrInit:
                    beeTable.append(Bee(len(beeTable)+1,int(cx),int(cy),0,0,0,0),cnt)
                    BeenrInit = False
                else:
                    if var:
                        var=False
                    # if((cx<1920/25*3)|(cy>1080/18*2)|(cx>1920/25*22)):
                    #     newbee = Bee(len(newBeeTable)+1,int(cx),int(cy),0,0,0,0)
                    #     newBeeTable.append(newbee)
                    #     beeTable.append(newbee)
                    #     ellipse = cv2.fitEllipse(cnt)
                    #     cv2.ellipse(frame, ellipse, (0,0,255),2)
                    #     cv2.putText(frame,str(newbee.id),(int(cx),int(cy)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
                    # if((cx>1920/25*3)&(cy<1080/18*2)&(cx<1920/25*22)): # > 230.4,< 950.4;
                    else:
                        testBee = Bee(len(testBeeTable)+1,int(cx),int(cy),0,0,2,0,cnt)
                        incr, beenr = Utils.checkDist(cx,cy,beeTable)

                        if(incr):
                            print('incr = True')
                            if(testBee.state==3):
                                testBee.counter+=1
                            else:
                                testBee.state = 3
                                testBeeTable.append(testBee)

                        else:
                            # k = k+1
                            # print(beenr)
                            currentBee = beeTable[beenr-1]
                            currentBee.speedX = currentBee.positionX-cx
                            currentBee.speedY = currentBee.positionY-cy
                            currentBee.newPosition(int(cx),int(cy))
                            print(beenr)
                            print(len(beeTable))
                            beeTable[beenr-1]=currentBee
                            currentBee.screen()
                            ellipse = cv2.fitEllipse(cnt)
                            cv2.ellipse(frame, ellipse, (0,0,255),2)
                            cv2.putText(frame,str(beenr),(int(cx),int(cy)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)


                # ellipsefit = True
                # if(ellipsefit):


                # print('cx:', int(cx), 'cy: ', int(cy))
                # bee = Bee(len(beeTable)+1, int(cx), int(cy),0,0)
                # incr, beenr = Utils.checkDist(cx,cy,beeTable)
                # if(incr):
                #     beeTable.append(bee)
                #     bee.screen()
                #

                # print(cnt)
                # print(cv2.contourArea(cnt))
                # newContours = [newContours, cv2.drawContours(frame, cnt, -1,(0,255,0),3)]
        cv2.imshow('newContours',frame)
        cv2.imshow('newContours',median)
        k=cv2.waitKey(30) & 0xFF
        if k ==27:
            break
cap.release()
cv2.destroyAllWindows()

# try the algorithm which is in the video, migth this be the migthy
