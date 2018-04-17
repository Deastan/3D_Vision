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

        j = 0
        for i in range(1, num_labels):  # don't do 0, cause it's just the background
            if stats[i, 4] > 2500:  # threshold to filter out small patches
                j += 1
                cv2.putText(original,str(i),(int(centroids[i,0]),int(centroids[i,1])), font, 1,(0,255,0),2,cv2.LINE_AA)###here i changed j to i in order to get the same number for the bee as in labels!!!
                cv2.ellipse(original, (int(centroids[i, 0]), int(centroids[i, 1])), (stats[i, 2] // 3, stats[i, 3] // 3), 0, 0, 360, 255, 2)

        return labels





    @staticmethod
    def defineROI(xMin, xMax, yMin, yMax, img):
        ROI=img[yMin: yMax, xMin:xMax]
        return ROI




    @staticmethod
    def getHistogram(realoriginal, label, blueArray, greenArray, redArray,frame):
        shadowPixels = []

        #get shadows
        for i, j in np.ndindex(labels.shape):
            if labels[i,j]==label:
                shadowPixels.append(realoriginal[i,j])
        shadowPixels=np.matrix(shadowPixels)

        shadowBlue = shadowPixels[:,0]
        shadowGreen = shadowPixels[:,1]
        shadowRed = shadowPixels[:,2]

        fig =plt.hist(shadowBlue,range=(0,255), normed=True, bins=255)

        # print(fig[0])
        # plt.show()
        blueArray+=fig[0]
        # plt.savefig('/home/philipp/Desktop/Histograms_shadows/shadwo_frame_'+str(frame)+'_label'+str(label)+'_blue')
        plt.hist(shadowGreen,range=(0,255), normed=True, bins=255)
        greenArray+=fig[0]
        # plt.show()
        # plt.savefig('/home/philipp/Desktop/Histograms_shadows/shadwo_frame_'+str(frame)+'_label'+str(label)+'_green')
        plt.hist(shadowRed,range=(0,255), normed=True, bins=255)
        redArray+=fig[0]
        # plt.show()
        plt.savefig('/home/philipp/Desktop/Histograms_bees/bee_frame'+str(frame)+'_label'+str(label)+'_red_or_ALL')
        return (blueArray, greenArray, redArray)





    @staticmethod
    def showCaughtPatch(realoriginal, labels, labelNumber):
        for i, j in np.ndindex(labels.shape):
            if labels[i,j]!= labelNumber:
                realoriginal[i,j]=(0,0,0)
