import numpy as np
import cv2
from cv2 import aruco
from matplotlib import pyplot as plt
import sys
sys.path.append('../utils/')

from calibration import *
# from feature_detection import *
from rendering import *
from video import *
import config as config
from objLoader_simple import *
from webcam import *

from aruco import *

camera_matrix, dist_coefs, rvecs, tvecs = calibrate()
cap = Webcam(0)
while True:
    frame = cap.getNextFrame()

    if frame is None:
        break

    rvecs, tvecs, frame = detect(frame, camera_matrix, dist_coefs)

    if len(rvecs) != 0 and len(tvecs) != 0:
        rvec = rvecs[0]
        tvec = tvecs[0]
        # frame = renderCube(frame, rvec, tvec, camera_matrix, dist_coefs)
        # frame = renderObj(frame, obj, rvec, tvec, camera_matrix, dist_coefs)

    frame = cv2.resize(frame, (1280, 720))

    cv2.imshow("",frame)
    if cv2.waitKey(1) == ord('q'):
        break
