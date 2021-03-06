import numpy as np
import cv2
import os
from Bee import Bee
from Utils import Utils

checkHisto = False

EntranceCounter = 0
ExitCounter = 0
coorYCrossingline = 570

# white: GOPR1406.MP4,
# not white: GOPR1400.MP4
videoName = 'GOPR1402.MP4'#'GOPR1352120FPS.MP4'
currentPath = os.getcwd()
videoPath = os.path.join('../../../Media',videoName)
window_name = 'bees'
# cv2.namedWindow(window_name)
# cv2.setMouseCallback(window_name, foo)

framenr = 0

cap = cv2.VideoCapture(videoPath)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

fgbg = cv2.createBackgroundSubtractorMOG2() #, varThreshold = 50)
entry = 0
exit = 0
beeTable = []
i = 0
incr = True
newBeeTable = []
testBeeTable = []
BeenrInit = True
var = False
lost = 5
anzBees = 0
beeIdmax = 0

while(1):


    ret, frame = cap.read()
    if framenr ==0:
        print(frame.shape)
        out = cv2.VideoWriter('tracking_test.avi',fourcc,10.0,(frame.shape[0:2]))

    # print(frame.shape)
    cv2.line(frame, (0,coorYCrossingline), (frame.shape[1],coorYCrossingline), (255, 0, 0), 2)
    framenr = framenr+1

    fgmask = fgbg.apply(frame)
    ret, thresh = cv2.threshold(fgmask,127,255,0)
    median = cv2.medianBlur(thresh,5)
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(median, kernel, iterations = 1)
    # plt.subplot(121),plt.imshow(frame),plt.title('Original')
    # plt.subplot(122),plt.imshow(median),plt.title('median')
    blur = cv2.GaussianBlur(dilation,(5,5),0)
    # print(blur.shape)
    newBeeTable = []
    img,contours, hierarchy = cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if contours !=[]:
        anzBees = len(beeTable)
        for cnt in contours:
            if (cv2.contourArea(cnt)>500)&(cv2.contourArea(cnt)<50000): #&(cv2.contourArea(cnt)<2500):
                isBee = True
                if checkHisto:
                    xCentr, yCentr, width, height = cv2.boundingRect(cnt)
                    isBee = Utils.checkColors(frame, xCentr, yCentr, width, height,median)
                if isBee:
                    M = cv2.moments(cnt)
                    cx = (M["m10"]/M["m00"])
                    cy = (M["m01"]/M["m00"])
                    if BeenrInit:
                        beeTable.append(Bee(len(beeTable),int(cx),int(cy),0,0,0,0,True,cnt))
                        # print('Hello', len(beeTable))
                    else:
                        newBeeTable.append(Bee(len(newBeeTable),int(cx),int(cy),0,0,0,0,True,cnt))

    beeIdmax = len(beeTable)

    if newBeeTable !=[]:
        for bee in beeTable:
            if newBeeTable !=[]:
                incr, beenr = Utils.checkDist(bee.positionX, bee.positionY,bee.counter, newBeeTable)
                if incr:
                    bee.state = 3
                    bee.update = False
                    bee.counter = bee.counter+1
                    beeTable[bee.id]=bee
                else:
                    # print('beeID', bee.id,'beenr', beenr)
                    newBee = newBeeTable[beenr]
                    newBeeTable.remove(newBee)
                    bee.state = 2
                    bee.counter = 0
                    bee.update = True
                    bee.historyPosition.append([bee.positionX,bee.positionY])
                    bee.speedX = newBee.positionX-bee.positionX
                    bee.speedY = newBee.positionY-bee.positionY
                    bee.cnt = newBee.cnt
                    oldY = bee.positionY
                    bee.newPosition(int(newBee.positionX),int(newBee.positionY))
                    if oldY<coorYCrossingline and bee.positionY>coorYCrossingline:
                        entry +=1
                    if oldY>coorYCrossingline and bee.positionY<coorYCrossingline:
                        exit +=1
                    beeTable[bee.id]=bee
                    # if (bee.id==17)|(bee.id==19):
                    #     x,y,w,h = cv2.boundingRect(bee.cnt)
                    #     cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

                    beeTableTest = beeTable[0:(beeTable.index(bee))]
                    # if (bee.id==17)|(bee.id==19):
                        # print(Utils.visible(bee, beeTableTest),'framenr: ',framenr)
                    if Utils.visible(bee, beeTableTest):
                        ellipse = cv2.fitEllipse(bee.cnt)
                        cv2.ellipse(frame, ellipse, (0,0,255),2)
                        cv2.putText(frame,str(bee.id),(int(bee.positionX),int(bee.positionY)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
    BeenrInit=False
    # for bee in beeTable:
    #     if bee.counter>10:


    cv2.putText(frame, "Entrances: {}".format(str(entry)), (10, 50),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(frame, "Exits: {}".format(str(exit)), (10, 70),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "# frame: {}".format(str(framenr)), (10, 90),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    for bee in newBeeTable:
        # if((bee.positionX<frame.shape[1]/25*3)|(bee.positionY<frame.shape[0]/18*5)|(bee.positionX>frame.shape[1]/25*22)):
        bee.id = len(beeTable)
        bee.state = 0
        beeTable.append(bee)
        if Utils.visible(bee,beeTable):
            ellipse = cv2.fitEllipse(bee.cnt)
            cv2.ellipse(frame, ellipse, (0,0,255),2)
            cv2.putText(frame,str(bee.id),(int(bee.positionX),int(bee.positionY)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
    # median = cv2.inRange(median, 50,255)
    # cv2.imshow(window_name,cv2.merge([frame[:,:,0]&median,frame[:,:,1]&median,frame[:,:,2]&median]))
    cv2.imshow('other',frame)
    # cv2.imshow('bees',median)
    # # cv2.imshow('newContours',median)
    if framenr%50==0:
        print('framenr: ',framenr,'exit: ',exit,'entry: ',entry)
    out.write(frame)
    k=cv2.waitKey(50) & 0xFF
    if k ==27:
        break
    # if framenr==401:
    #     break
    # if framenr == 64 or framenr ==126 or framenr ==188 or framenr ==250 or framenr==312 or framenr ==347:
    #     print('entrance: ', entry, 'exit', exit, 'framenr: ', framenr)
cap.release()
out.release()
cv2.destroyAllWindows()

# try the algorithm which is in the video, migth this be the migthy
