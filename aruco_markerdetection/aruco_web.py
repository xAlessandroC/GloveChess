import numpy as np
import cv2
from cv2 import aruco
from matplotlib import pyplot as plt

from utils.calibration import *
from utils.feature_detection import *
from utils.rendering import *
from utils.video import *
import utils.config as config
from utils.objLoader_simple import *
from utils.webcam import *

from aruco_markerdetection.aruco import *

camera_matrix, dist_coefs, rvecs, tvecs = calibrate()
obj = OBJ(config.obj_path)
cap = Webcam(0)
while True:
    frame = cap.getNextFrame()

    if frame is None:
        break

    rvecs, tvecs, frame, center, projection = detect(frame, camera_matrix, dist_coefs, None)

    if len(rvecs) != 0 and len(tvecs) != 0:
        rvec = rvecs[0]
        tvec = tvecs[0]
        frame = renderCube(frame, rvec, tvec, camera_matrix, dist_coefs)
        # frame = renderObj(frame, obj, rvec, tvec, camera_matrix, dist_coefs)

    frame = cv2.resize(frame, (1280, 720))

    cv2.imshow("",frame)
    if cv2.waitKey(1) == ord('q'):
        break
