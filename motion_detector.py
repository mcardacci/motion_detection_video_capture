import argparse
import datetime
import imutils
import time 
import cv2

# construct the arg parser that takes from the command line 
ap=argparse.ArgumentParser()
# here we can parse from a pre-recorded video
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args=vars(ap.parse_args())

# if the video arg is None, then we are reading from webcam
if args.get("video", None) is None:
	camera=cv2.VideoCapture(0)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera=cv2.VideoCapture(args["video"])

# initialize the first frame in the video
firstFrame=None

# loop over the frames of the video
while True:
	# print "video is being captured"
	# Grab the vurrent frame and initilize the occupied/unoccupied
	# text
	(grabbed, frame)=camera.read()
	text="Unoccupied"

	# If frame couldn't be grabbed, then we've reached 
	# the end of the video
	if not grabbed:
		break

	# Resize the frame, convert it to grayscale, and blur it
	frame=imutils.resize(frame, width=500)
	gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray=cv2.GaussianBlur(gray, (21, 21), 0)

	# If the first frame is None, initialize it
	if firstFrame is None:
		firstFrame=gray
		continue

	# Compute the absolute difference between the current frame and 'firstFrame'
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# Loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# Compute the bounding box for the counter, draw it on the frame and update the text
		(x, y, w, h)=cv2.boundingRect(c)
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
		text="Occupied"

	#draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I %M:%S%p"), (10,frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	
	# Show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# If the q key is pressed, break from the loop
	if key==ord("q"):
		break

# Cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
