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
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# If the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# Compute the absolute difference between the current frame and 'firstFrame'
	# Larger frame deltas indicate that motion is taking place
	frameDelta = cv2.absdiff(firstFrame, gray)
	# Here we threshold the frame delta to reveal the regions of the image that only have significant changes in pixel intensity
	# If the threshold is less than 25, we discard it and set it to black (background), else we set it to white (foreground)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)

	# Here we apply contour detection to find the outlines of these white regions
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTE

	# Loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it bc they're irrelevant
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# Compute the bounding box for the counter, draw it on the frame and update the text
<<<<<<< HEAD
		(x, y, w, h)=cv2.boundingRect(c)
		# If the contour area is larger than our supplied '--min-area', draw the box surrounding the foreground and motion region
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
		text="Occupied"

	#draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I %M:%S%p"), (10,frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	
	# Show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

# Example call:
# python motion_detector.py --video videos/example_01.mp4