from pyimagesearch.tempimage import tempimage
from dropbox.client import DropboxOAuth2FlowNoRedirect
from dropbox.client import DropboxClient
from picamera.array import PiRGBArray
from picamera import picamera
import argparse
import warnings 
import datetime
import imutils
import json
import time
import cv2

# make arg parser and parse argparse
ap=argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
args=vars(ap.parse_args())

# filter warnings, load the configuration and init D.Box client
warnings.filterwarnings("ignore")
conf=json.load(open(args["conf"]))
client=None