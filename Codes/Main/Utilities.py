from Bee import Bee
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import sys

class Utilities:



    @staticmethod
    def connectedComponents(fgmask, original, connectivity=4, beesTable=[]):
        font = cv2.FONT_HERSHEY_SIMPLEX
        global labels


        output = cv2.connectedComponentsWithStats(fgmask, connectivity, cv2.CV_32S)

        num_labels = output[0]
        labels = output[1]
        stats = output[2]
        centroids = output[3]

        fgmask = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
        j = 0
        for i in range(1, num_labels):  # don't do 0, cause it's just the background
            if stats[i, 4] > 2500:  # threshold to filter out small patches
                j += 1
                bee = Bee(len(beesTable)+1, int(centroids[i,0]), int(centroids[i,1]), 0, 0) # create a bee and
                bee.screen() # screen during the test
                beesTable.append(bee) # add to the table of bees 
                cv2.putText(original,str(j),(int(centroids[i,0]),int(centroids[i,1])), font, 1,(0,255,0),2,cv2.LINE_AA)
                cv2.ellipse(original, (int(centroids[i, 0]), int(centroids[i, 1])), (stats[i, 2] // 3, stats[i, 3] // 3), 0, 0, 360, 255, 2)



    @staticmethod
    def defineROI(xMin, xMax, yMin, yMax, img):
        ROI=img[yMin: yMax, xMin:xMax]
        return ROI

    global histoMatrix
    #The histomatrix contains 0)the considered frames, 1)the labels being shadows in this frame 2) the labels being bees in this frame
    histoMatrix= np.matrix([[[4],[5],[6],[24]],  [[2,3],[2,3],[1,4],[3],]  ,[[1],[1],[2,3],[1,2]]])




    @staticmethod
    def getHistogram(original):
        global histoMatrix
        shadowPixels = []

        #get shadows
        for i, j in np.ndindex(labels.shape):
            if labels[i,j]==histoMatrix[1,0][0]:
                shadowPixels.append(original[i,j])
        print("done")
        shadowPixels=np.matrix(shadowPixels)

        shadowBlue = shadowPixels[:,0]
        shadowGreen = shadowPixels[:,1]
        shadowRed = shadowPixels[:,2]

        histoBlue=plt.hist(shadowBlue, normed=True, bins=79)
        histoGreen=plt.hist(shadowGreen, normed=True, bins=79)
        histoRed=plt.hist(shadowRed, normed=True, bins=79)

        print(histoBlue)
        plt.show()
        
    @staticmethod
    def calculateDistorsion(path):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        
        #path = '/home/jonathan/git/3D_Vision/JohnVideos/calibration_easter_hive'
        os.chdir(path)
        images = glob.glob('*.JPG')
        
        print(images)
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
        
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
        
                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2)
                print(fname)
        
                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
                cv2.imshow('img',img)
                cv2.waitKey(500)
        
        cv2.destroyAllWindows()
        
        # returns the: camera matrix, distortion coefficients, rotation and translation vectors
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        np.save('ret',ret)
        np.save('mtx',mtx)
        np.save('dist',dist)
        np.save('rvecs',rvecs)
        np.save('tvecs',tvecs)


     # This code plays a distorted video with the distortion parameters calculated from another video with the size 1920x1080
    @staticmethod
    def calibrateVideo(path):
        
        
        # Load the calibration parameters
        ret = np.load('ret.npy')
        mtx = np.load('mtx.npy')
        dist = np.load('dist.npy')
        rvecs = np.load('rvecs.npy')
        tvecs = np.load('tvecs.npy')
        
        # Load the video
        cap = cv2.VideoCapture(path) # Place the name of the video you want to play
        
        while(1):
            ret, frame = cap.read()
        
            frame = cv2.resize(frame,(1920,1080),interpolation=cv2.INTER_LINEAR) # Adapt the imagesize
            h,  w = frame.shape[:2]
        
            newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
            dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        
            # show both videos the original called 'frame' and the undistorted called 'dist'
            cv2.imshow('frame',frame)
            cv2.imshow('dist',dst)
            k = cv2.waitKey(1)&0xFF
            if k ==27:
                break
        
        cap.release()
        cv2.destroyAllWindows()
