import numpy as np
import cv2

cap = cv2.VideoCapture('/home/philipp/Desktop/Avril/GOPR1334.MP4')
fgbg = cv2.createBackgroundSubtractorMOG2()
font = cv2.FONT_HERSHEY_SIMPLEX
fourcc = cv2.VideoWriter_fourcc(*'XVID') # Define the codec and create VideoWriter object (fourcc)
init=0
counter = 0


def centroid(img):
    x_tot=0
    y_tot=0
    counter=0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j]!=0:
                x_tot+=i
                y_tot+=j
                counter+=1
    x=x_tot//counter
    y=y_tot//counter
    return x,y





while(1):
    ret, original = cap.read()
    counter+=1




    fgmask = fgbg.apply(original)
    ret, fgmask_threshold = cv2.threshold(fgmask, 120, 255, cv2.THRESH_BINARY)

    fgmask_median= cv2.medianBlur(fgmask_threshold, 9)

    x,y=centroid(fgmask_median)

    fgmask = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)#make it have 3 channels => same matrix dimensions

    fgmask_median = cv2.cvtColor(fgmask_median, cv2.COLOR_GRAY2BGR)
    fgmask_threshold = cv2.cvtColor(fgmask_threshold, cv2.COLOR_GRAY2BGR)
    fgmask_median=cv2.circle(fgmask_median,(y,x),40,(0,0,255),5)
    cv2.putText(original, 'Original', (100, 100), font, 4, (255, 255, 255), 2, cv2.LINE_AA)#org is the bottom left corner of the text in the image (in pixels)
    cv2.putText(fgmask, 'fgmask', (100, 100), font, 4, (255, 255, 255), 2, cv2.LINE_AA)#org is the bottom left corner of the text in the image (in pixels)
    cv2.putText(fgmask_median, 'fgmask_median', (100, 100), font, 4, (255, 255, 255), 2, cv2.LINE_AA)#org is the bottom left corner of the text in the image (in pixels)
    cv2.putText(fgmask_threshold, 'fgmask_threshold', (100, 100), font, 4, (255, 255, 255), 2, cv2.LINE_AA)#org is the bottom left corner of the text in the image (in pixels)


    tmp1 = np.hstack((original, fgmask))
    tmp2 = np.hstack((fgmask_median, fgmask_threshold))
    allTogether = np.vstack((tmp1, tmp2))
    if init==0:
        out = cv2.VideoWriter('/home/philipp/Desktop/video_circle.avi',fourcc, 3.0,(allTogether.shape[1],allTogether.shape[0])) #define: format, fps, and frame-size (pixels)
        init=1
    out.write(allTogether)
    if counter==8 or counter ==9:
        cv2.imwrite('/home/philipp/Desktop/image_original'+str(counter)+'.jpg', original)
        cv2.imwrite('/home/philipp/Desktop/image_fgmask'+str(counter)+'.jpg', fgmask)
        cv2.imwrite('/home/philipp/Desktop/image_fgmask_median'+str(counter)+'.jpg', fgmask_median)
        cv2.imwrite('/home/philipp/Desktop/image_fgmask_threshold'+str(counter)+'.jpg', fgmask_threshold)
    if counter==9:
        break



    cv2.namedWindow('frame_median',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame_median', 1200,800)
    cv2.imshow('frame_median', allTogether)


    k = cv2.waitKey(1) & 0xff#modify the frame-speed
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
