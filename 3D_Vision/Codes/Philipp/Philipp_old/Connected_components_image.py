import cv2
import numpy as np
import collections
import time

# img = cv2.imread('/home/philipp/Desktop/image.png', 0)
img67 = cv2.imread('/home/philipp/Desktop/white.jpg', 1)
img=cv2.cvtColor(img67, cv2.COLOR_BGR2GRAY)

cv2.imshow('1', img)
cv2.waitKey()

img = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)[1]  # ensure binary
ret, labels = cv2.connectedComponents(img)
#
# count = [0 for x in range(max(labels))]
# for i, j in np.ndindex(labels.shape):
#     count[img[i,j]] += 1
# print(count)
# print(sum(count))

# Map component labels to hue val
label_hue = np.uint8(179*labels/np.max(labels))
blank_ch = 255*np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

# cvt to BGR for display
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)




# set bg label to black
labeled_img[label_hue==0] = 0

cv2.imshow('labeled.png', labeled_img)
cv2.waitKey()
