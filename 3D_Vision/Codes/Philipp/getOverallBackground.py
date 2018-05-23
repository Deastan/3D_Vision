import numpy as np
import cv2


cap = cv2.VideoCapture('/home/philipp/Desktop/GOPR1345.MP4')
counter=0
n=500

while(cap.isOpened()):
    ret, frame = cap.read()
    if counter==0:
        global averageImage
        averageImage=np.zeros(frame.shape)
    averageImage+=(frame/n)
    print ("\r frame"+str(counter),end= "")
    counter+=1
    if counter==n:
        break


newAverage = np.zeros(frame.shape, np.uint8)
for i, j ,k in np.ndindex(newAverage.shape):
    newAverage[i,j,k] = averageImage[i,j,k]



cap.release()

cv2.imshow('windowName', newAverage)
cv2.imwrite('/home/philipp/Desktop/average.jpg', newAverage)
cv2.waitKey(0)
cv2.destroyAllWindows()
