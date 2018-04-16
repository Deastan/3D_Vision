from Bee import Bee
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import sys

class Utilities:


# ************************************************************
# Function for tracking
# ************************************************************

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

# ************************************************************
# Function which calculate the different componants for the distorsion of the camera
# ************************************************************

    @staticmethod
    def calculateDistorsion():
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
        images = glob.glob('../../Media/*.JPG')
        assert (imgages), "The images for caluclateDistorion can't be loaded. Please check if you put the Pictures as JPG in Media"

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
        np.save('Calibration/ret',ret)
        np.save('Calibration/mtx',mtx)
        np.save('Calbiration/dist',dist)
        np.save('Calibration/rvecs',rvecs)
        np.save('Calibration/tvecs',tvecs)

# ************************************************************
# Calibrate the video from the calculus from the distorsion function
# ************************************************************

    @staticmethod
    def calibrateVideo(path):
    # This code plays a distorted video with the distortion parameters calculated
    # from another video with the size 1920x1080


        # Load the calibration parameters
        ret = np.load('Calibration/ret.npy')
        mtx = np.load('Calibration/mtx.npy')
        dist = np.load('Calibration/dist.npy')
        rvecs = np.load('Calibration/rvecs.npy')
        tvecs = np.load('Calibration/tvecs.npy')
        # assert((ret==[])&(mtx==[])&(dist==[])&(rvecs==[])&(tvecs==[])), "Can't find the parameters for undistorting the image"
        # Load the video
        cap = cv2.VideoCapture(path) # Place the name of the video you want to play
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output_05.avi',fourcc, 20.0, (1920,1080))

        while(cap.isOpened()):
            ret, frame = cap.read()

            frame = cv2.resize(frame,(1920,1080),interpolation=cv2.INTER_LINEAR) # Adapt the imagesize
            h,  w = frame.shape[:2]

            newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
            dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)

            # show both videos the original called 'frame' and the undistorted called 'dist'
            #cv2.imshow('frame',frame)
            #cv2.imshow('dist',dst)

            # saved videos
            if ret==True:
                out.write(dst)

                cv2.imshow('dst',frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            else:
                break
            # other stuff
            k = cv2.waitKey(1)&0xFF
            if k ==27:
                break

        #print("The video is recording !")
        #Utilities.saveVideo("output_01")
        #print("The riccord is finished !")

        cap.release()
        cv2.destroyAllWindows()

# ************************************************************
# Save the video
# ************************************************************

    @staticmethod
    def saveVideo(name):
        cap = cv2.VideoCapture(0)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(name + '.avi',fourcc, 20.0, (1920,1080))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                frame = cv2.flip(frame,0)

                # write the flipped frame
                out.write(frame)

                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()


# ************************************************************
# Tracking
# ************************************************************

        # Code from Philipp
    @staticmethod
    def trackingPhilipp(path):
        cap = cv2.VideoCapture(path)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Define the codec and create VideoWriter object (fourcc)
        init = 0
        fgbg = cv2.createBackgroundSubtractorMOG2()
        counter = 0
        beesTable1 = [] # table which content the bees

        while (1):


            ret, original = cap.read()

            # if init == 0:
            #     out = cv2.VideoWriter('/home/philipp/Desktop/video_circle.avi', fourcc, 10, (original.shape[1], original.shape[0]))  # define: format, fps, and frame-size (pixels)
            #     init = 1
            # out.write(original)


            # original = Utilities.defineROI(100,1700,500,750,original)

            # create bg-subtracted, thresholded and median-filtered image
            fgmask = fgbg.apply(original)
            fgmask = cv2.medianBlur(fgmask, 9)
            ret, fgmask = cv2.threshold(fgmask, 120, 255, cv2.THRESH_BINARY)
            kernel = np.ones((35, 35), np.uint8)
            # erosion = cv2.erode(fgmask,kernel,iterations = 1)
            # fgmask = cv2.dilate(fgmask, kernel, iterations=1)



            Utilities.connectedComponents(original=original,fgmask=fgmask, connectivity=8, beesTable=beesTable1)

            cv2.putText(original, "frame:" +str(counter+1),(50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.namedWindow('frame_median', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame_median', 1200, 800)
            cv2.imshow('frame_median', original)



            # labels=labels*50000
            # cv2.imshow('frame_median', labels)
            # if counter==2:
            #     cv2.imwrite('/home/philipp/Desktop/white.jpg',original)
            #     break


        #*************************************
        # There is an error in these 2 next line
        #*************************************
            #counter += 1
            #print("\r frame" + str(counter), end="")

            #
            # # time.sleep(1)
            # if counter==4:
            #     Utilities.getHistogram(original)
            #     break


            k = cv2.waitKey(1) & 0xff  # modify the frame-speed
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
