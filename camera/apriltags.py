
import numpy as np
from pupil_apriltags import Detector
from stream import Stream
from tag import Tag
import cv2
from time import sleep, time
from picamera import PiCamera
from argparse import ArgumentParser
from pdb import set_trace
import time
import imghdr

# Get time of stream and name for saving outputs
# parser = ArgumentParser()
# parser.add_argument("-rn", "--run_name", type=str, required=True)
# parser.add_argument("-t", "--run_time", type=int)
# args = parser.parse_args()
# if args.run_time:
#     MAX_TIME = args.run_time
# else:
#     MAX_TIME = 4
MAX_TIME = 4
run_name = "April Tags shit"
# Camera information
FPS = 30
RES = (640, 480)
camera_info = {}
# Camera Resolution
camera_info["res"] = RES
camera_info["K"] = np.array([[314.22174729465604, 0.0, 337.0278425306902],
                             [0.0, 311.4202447283487, 238.99954338265644],
                             [0.0, 0.0, 1.0]])
camera_info["D"] = np.array([[-0.03953861358665185],
                             [0.014918638704331555],
                             [-0.022402610396196412],
                             [0.00863418416543917]])

cap = cv2.VideoCapture('/dev/video0')
cap.set(3,640);
cap.set(4,480);


cap.get(8)

# Camera Intrinsic Matrix (3x3)
# The non-default elements of the K array, in the AprilTag specification
camera_info["params"] = [1.13681104 * 10 ** 3, 1.13670829 * 10 ** 3, 9.61298528 * 10 ** 2, 5.50718212 * 10 ** 2]
# Fisheye Camera Distortion Matrix

# Tag information
TAG_SIZE = .170
FAMILIES = "tag36h11"
tags = Tag(TAG_SIZE, FAMILIES)
# Add information about tag locations
# Function Arguments are id,x,y,z,theta_x,theta_y,theta_z
tags.add_tag(0, 76.25, 30.5, 0., 0., 0., 0.)
# tags.add_tag(1, 115., 31.5, 0., 0., 0., 0.)
# tags.add_tag(2, 95.75, 50., 0., 0., 0., 0.)
# tags.add_tag(3, 0., 41., 38.75, 0., -np.pi / 2, 0.)
# tags.add_tag(4, 0., 54., 19.25, 0., -np.pi / 2, 0.)


# this is wrong. Fuck you matthew
starting_position = np.array([[.635], [1.0668], [2.7432]])

# Create Apriltags Detector
detector = Detector(families=tags.family, nthreads=4)

# Create the camera object

# Reduce the shutter speed to reduce blur, given in microseconds
cap.set(15, int(1000000 / (3 * FPS)))
    # Create the stream object
stream = Stream(detector, camera_info, tags, starting_position, run_name)
sleep(1)
print("Starting")
# try:
while True:
    # Start recording frames to the stream object
    ret, frame = cap.read()
    if (ret):
        #imghdr.what(frame)
        print("writing frame")
        stream.write(frame)


# except Exception as e:
#     print(e)
# Print Timing Information
stream.print_statistics(MAX_TIME)
# Save camera frames with detections overlaid
stream.save_video(MAX_TIME)
# Save position numpy arrays
stream.save_positions()
# Create scatter plot of estimated positions
stream.scatter_position()
# Animate the stream to show the camera moving in real time
# stream.animate_position(MAX_TIME)

set_trace()
