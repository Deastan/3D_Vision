# import the necessary packages
import math
import numpy as np
import argparse
import datetime
import imutils
import time
import cv2
 
#global variables
width = 0
height = 0
EntranceCounter = 0
ExitCounter = 0
MinCountourArea = 30  #Adjust ths value according to your usage
BinarizationThreshold = 150  #Adjust ths value according to your usage
OffsetRefLines = 150  #Adjust ths value according to your usage

#Check if an object in entering in monitored zone
def CheckEntranceLineCrossing(y, CoorYEntranceLine, CoorYExitLine):
    AbsDistance = abs(y - CoorYEntranceLine)	

    if ((AbsDistance <= 2) and (y < CoorYExitLine)):
     return 1
    else:
     return 0

#Check if an object in exitting from monitored zone
def CheckExitLineCrossing(y, CoorYEntranceLine, CoorYExitLine):
    AbsDistance = abs(y - CoorYExitLine)	

    if ((AbsDistance <= 2) and (y > CoorYEntranceLine)):
     return 1
    else:
     return 0
#plot reference lines (entrance and exit lines) 
CoorYEntranceLinefloat = (height / 2)-OffsetRefLines
CoorYExitLinefloat = (height / 2)+OffsetRefLines
CoorYEntranceLine = np.round(CoorYEntranceLinefloat).astype('int')
CoorYExitLine = np.round(CoorYExitLinefloat).astype('int')
#cv2.line(frame, (0,CoorYEntranceLine), (width,CoorYEntranceLine), (255, 0, 0), 2)
#cv2.line(frame, (0,CoorYExitLine), (width,CoorYExitLine), (0, 0, 255), 2)
# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video", help="C:\\Users\\julie\\Desktop\\3D_Vision\\Media\\GOPR1345.MP4")
#ap.add_argument("-a", "--min-area", type=int, default=500, help=40)
#args = vars(ap.parse_args())
 
# if the video argument is None, then we are reading from webcam
#if args.get("video", None) is None:
#	camera = cv2.VideoCapture(0)
#	time.sleep(0.25)
 
# otherwise, we are reading from a video file
#else:
camera = cv2.VideoCapture('C:\\Users\\julie\\Desktop\\3D_Vision_copie\\Media\\GOPR1345.MP4')
 
# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	text = "Unoccupied"
 
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break
 
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue
    
	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
 
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 2:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
(x, y, w, h) = cv2.boundingRect(c)
cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		#text = "Occupied"
cv2.line(frame, (0,CoorYEntranceLine), (width,CoorYEntranceLine), (255, 0, 0), 2)
cv2.line(frame, (0,CoorYExitLine), (width,CoorYExitLine), (0, 0, 255), 2)
        #find object's centroid
CoordXCentroid = (x+x+w)/2
CoordYCentroid = (y+y+h)/2
ObjectCentroidfloat = (CoordXCentroid,CoordYCentroid)
ObjectCentroid = (np.round(CoordXCentroid).astype('int'),np.round(CoordYCentroid).astype('int'))
cv2.circle(frame, ObjectCentroid, 1, (0, 0, 0), 5)
if (CheckEntranceLineCrossing(CoordYCentroid,CoorYEntranceLine,CoorYExitLine)):
        EntranceCounter += 1

if (CheckExitLineCrossing(CoordYCentroid,CoorYEntranceLine,CoorYExitLine)):  
        ExitCounter += 1

#    print "Total countours found: " + str(QttyOfContours)

    #Write entrance and exit counter values on frame and shows it
cv2.putText(frame, "Entrances: {}".format(str(EntranceCounter)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
cv2.putText(frame, "Exits: {}".format(str(ExitCounter)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
cv2.imshow("Original Frame", frame)
cv2.waitKey(1);
        
	# draw the text and timestamp on the frame
	#cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		#cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	#cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		#(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	# show the frame and record if the user presses a key
	#cv2.imshow("Security Feed", frame)
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)
	#key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key is pressed, break from the lop
	#if key == ord("q"):
		#break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()        
