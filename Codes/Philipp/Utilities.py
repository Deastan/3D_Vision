import cv2
import numpy as np
import matplotlib.pyplot as plt

class Utilities:



    @staticmethod
    def connectedComponents(fgmask, original, connectivity=4):
        font = cv2.FONT_HERSHEY_SIMPLEX
        global labels


        output = cv2.connectedComponentsWithStats(fgmask, connectivity, cv2.CV_32S)

        num_labels = output[0]
        labels = output[1]
        stats = output[2]
        centroids = output[3]

        fgmask = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)

        # j = 0
        # for i in range(1, num_labels):  # don't do 0, cause it's just the background
        #     if stats[i, 4] > 2500:  # threshold to filter out small patches
        #         j += 1
                # cv2.putText(original,str(j),(int(centroids[i,0]),int(centroids[i,1])), font, 1,(0,255,0),2,cv2.LINE_AA)
                # cv2.ellipse(original, (int(centroids[i, 0]), int(centroids[i, 1])), (stats[i, 2] // 3, stats[i, 3] // 3), 0, 0, 360, 255, 2)
                # cv2.putText(original, str(j), (int(centroids[i, 0]), int(centroids[i, 1])), font, 1, (0, 255, 0), 2, cv2.LINE_AA)



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


