import numpy as np
import cv2
from cv2 import aruco
from matplotlib import pyplot as plt

from utils.calibration import *
from utils.feature_detection import *
from utils.rendering import *
from utils.video import *
from utils.paths import *
from utils.objLoader import *

from aruco import *

camera_matrix, dist_coefs, rvecs, tvecs = calibrate()
obj = OBJ(obj_path)
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()

    if not ret or frame is None:
        # Release the Video if ret is false
        cap.release()
        print("Released Video Resource")
        break

    rvec, tvec, frame, center, projection = detect(frame, camera_matrix, dist_coefs, None)

    if len(rvec) != 0 and len(tvec) != 0:
        # frame = renderCube(frame, rvec, tvec, camera_matrix, dist_coefs)
        frame = renderObj(frame, obj, rvec, tvec, camera_matrix, dist_coefs)

    frame = cv2.resize(frame, (1280, 720))

    cv2.imshow("",frame)
    if cv2.waitKey(1) == ord('q'):
        break
