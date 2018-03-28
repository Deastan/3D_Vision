import numpy as np
import cv2
import glob

ret = np.load('ret.npy')
mtx = np.load('mtx.npy')
dist = np.load('dist.npy')
rvecs = np.load('rvecs.npy')
tvecs = np.load('tvecs.npy')

img = cv2.imread('frame29.png')
h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# cv2.imshow('dst',dst)
# cv2.waitKey(5000) & 0xFF
# cv2.imwrite('dist.png', dst)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('calibresult.png',dst)

cal = cv2.imread('calibresult.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('cal',cal)
cv2.waitKey(5000) & 0xFF
