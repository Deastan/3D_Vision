import cv2
import numpy as np

image = cv2.imread('bees.png')
# bg = image[650:800,700:1100] # the whole image
# bees = cv2.imread('bees.png')[905:975,950:975]
foregr = cv2.imread('fg.png',0)
back = cv2.imread('background.png',0)
# while(1):
#     # cv2.imshow('bg', bg)
#     # cv2.imshow('bee', bees)
#     # cv2.imshow('image',image)
#     cv2.imshow('back',back)
#     cv2.imshow('foregr',foregr)
#     k = cv2.waitKey(500)&0xFF
#     if k == 27:
#         break

# cv2.imwrite('beescut.png', image)
cv2.destroyAllWindows()
bg = np.zeros((1,65),np.float64)
bees = np.zeros((1,65),np.float64)
mask = np.zeros(image.shape[:2],np.uint8)
mask[mask==0]=2
mask[foregr==0] = 1
mask[back==0] = 0

# test = [foregr==255]*image
# while(1):
#     cv2.imshow('test',test)
#
#     k = cv2.waitKey(500)&0xFF
#     if k == 27:
#         break

# cv2.imwrite('beescut.png', image)
cv2.destroyAllWindows()

print(mask, np.max(mask), np.min(mask))
# mask[905:975,950:975] = 1
rect = ((905+975)/2,(950+975)/2,975-905,975-950)
cv2.grabCut(image,mask,None,bg,bees,10,cv2.GC_INIT_WITH_MASK)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
image2 = image*mask2[:,:,np.newaxis]

while(1):
    # cv2.imshow('bg', bg)
    # cv2.imshow('bee', bees)
    # cv2.imshow('image',image)
    cv2.imshow('image2',image2)
    # cv2.imshow('img',img)
    k = cv2.waitKey(500)&0xFF
    if k == 27:
        break

# cv2.imwrite('beescut.png', image)
cv2.destroyAllWindows()
