import numpy as np
import cv2
import glob

#Part 1 saving pictures from videos

# save the video to images
import cv2
print(cv2.__version__)
vidcap = cv2.VideoCapture('GOPR1326.MP4')
success,image = vidcap.read()
count = 0
i=0
success = True
while success:
    if count%20==1:
        print(count,i)
        i+=1
        cv2.imwrite("frame%d.png" % i, image)     # save frame as JPEG file
    success,image = vidcap.read()
    # print 'Read a new frame: ', success
    count += 1
