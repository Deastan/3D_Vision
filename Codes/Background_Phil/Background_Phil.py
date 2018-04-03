import numpy as np
import cv2

cap = cv2.VideoCapture('/home/philipp/Desktop/GOPR1292.MP4')
fgbg = cv2.createBackgroundSubtractorMOG2()
font = cv2.FONT_HERSHEY_SIMPLEX



while(1):
    ret, original = cap.read()
    fgmask = fgbg.apply(original)
    fgmask_median= cv2.medianBlur(fgmask, 9)
    ret, fgmask_threshold = cv2.threshold(fgmask, 120, 255, cv2.THRESH_BINARY)

    #make it have 3 channels => same matrix dimension
    fgmask = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)

    #create thresholded image, median-filtered
    fgmask_median = cv2.cvtColor(fgmask_median, cv2.COLOR_GRAY2BGR)
    fgmask_threshold = cv2.cvtColor(fgmask_threshold, cv2.COLOR_GRAY2BGR)

    #Add text to the images
    cv2.putText(original, 'Original', (100, 100), font, 4, (255, 255, 255), 2, cv2.LINE_AA)#org is the bottom left corner of the text in the image (in pixels)
    cv2.putText(fgmask, 'fgmask', (100, 100), font, 4, (255, 255, 255), 2, cv2.LINE_AA)#org is the bottom left corner of the text in the image (in pixels)
    cv2.putText(fgmask_median, 'fgmask_median', (100, 100), font, 4, (255, 255, 255), 2, cv2.LINE_AA)#org is the bottom left corner of the text in the image (in pixels)
    cv2.putText(fgmask_threshold, 'fgmask_threshold', (100, 100), font, 4, (255, 255, 255), 2, cv2.LINE_AA)#org is the bottom left corner of the text in the image (in pixels)

    #put all images together in one
    tmp1 = np.hstack((original, fgmask))
    tmp2 = np.hstack((fgmask_median, fgmask_threshold))
    allTogether = np.vstack((tmp1, tmp2))

    #show frames and change window size
    cv2.namedWindow('frame_median',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame_median', 1200,800)
    cv2.imshow('frame_median', allTogether)


    k = cv2.waitKey(1) & 0xff#modify the frame-speed
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
