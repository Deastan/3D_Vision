import numpy as np
import cv2
import time

cap = cv2.VideoCapture('/home/jonathan/Desktop/Videos/GOPR1353FPS60.MP4')
fourcc = cv2.VideoWriter_fourcc(*'XVID') # Define the codec and create VideoWriter object (fourcc)
init=0
fgbg = cv2.createBackgroundSubtractorMOG2()
font = cv2.FONT_HERSHEY_SIMPLEX
counter=0



while(1):
    ret, original = cap.read()

    #create bg-subtracted, thresholded and median-filtered image
    fgmask = fgbg.apply(original)
    fgmask= cv2.medianBlur(fgmask, 9)
    ret, fgmask = cv2.threshold(fgmask, 120, 255, cv2.THRESH_BINARY)

    kernel = np.ones((40,40),np.uint8)
    # erosion = cv2.erode(fgmask,kernel,iterations = 1)
    fgmask = cv2.dilate(fgmask,kernel,iterations = 1)


# You need to choose 4 or 8 for connectivity type
    connectivity = 8
# Perform the operation
    output = cv2.connectedComponentsWithStats(fgmask, connectivity, cv2.CV_32S)
# Get the results
# The first cell is the number of labels
    num_labels = output[0]
# The second cell is the label matrix
    labels = output[1]
# The third cell is the stat matrix
    stats = output[2]
# The fourth cell is the centroid matrix
    centroids = output[3]
    fgmask=cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
    j=0
    for i in range(1,num_labels): #don't do 0, cause it's just the background
        if stats[i,4]>2500: #threshold to filter out small patches
            j+=1
            # cv2.circle(original,(int(centroids[i,0]),int(centroids[i,1])), stats[i,4]//30, (0,0,255), 2)
            # cv2.putText(original,str(j),(int(centroids[i,0]),int(centroids[i,1])), font, 1,(0,255,0),2,cv2.LINE_AA)

            # cv2.circle(original,(int(centroids[i,0]),int(centroids[i,1])), 30, (0,0,255), 2)
            cv2.ellipse(original,(int(centroids[i,0]),int(centroids[i,1])),(stats[i,2]//3,stats[i,3]//3),0,0,360,255,2)
            cv2.putText(original,str(j),(int(centroids[i,0]),int(centroids[i,1])), font, 1,(0,255,0),2,cv2.LINE_AA)


    cv2.namedWindow('frame_median',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame_median', 1200,800)

    cv2.imshow('frame_median', original)

    # labels=labels*50000
    # cv2.imshow('frame_median', labels)

    if init==0:
        out = cv2.VideoWriter('/home/philipp/Desktop/video_circle.avi',fourcc, 10,(original.shape[1],original.shape[0])) #define: format, fps, and frame-size (pixels)
        init=1
    out.write(original)
    #
    # if counter==3:
    #     cv2.imwrite('/home/philipp/Desktop/fgmask.jpg',fgmask)

    counter+=1
    print ("\r frame"+str(counter),end= "")


    k = cv2.waitKey(1) & 0xff#modify the frame-speed
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
