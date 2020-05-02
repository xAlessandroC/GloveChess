"""
    This module implements the recognition of an Aruco marker. The returned rvec and tvec are the results of
    a filtering step performed by marker_stabilizer module.
"""

import cv2
import numpy as np

from cv2 import aruco
from marker_stabilizer import *

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
size_marker = 8.0

def detect(frame, camera_matrix, dist_coefs):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame_gray, aruco_dict, parameters=parameters)

    rendered_img = frame
    rvecs = []
    tvecs = []
    rvec = []
    tvec = []
    if corners != []:
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, size_marker, camera_matrix, dist_coefs)

        # Hypothesis: we have only the chessboard marker, so we take only the first result
        rvec = rvecs[0]
        tvec = tvecs[0]
        rendered_img = aruco.drawAxis(rendered_img, camera_matrix, dist_coefs, rvec, tvec, 10.0)

        rvec, tvec = getCorrectVectors(rvec, tvec)
    else:
        rvec, tvec = getCorrectVectors(rvec, tvec)

    return (np.array([rvec]), np.array([tvec]), rendered_img)
