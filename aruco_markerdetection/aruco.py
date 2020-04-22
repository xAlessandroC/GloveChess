import numpy as np
import cv2
from cv2 import aruco
from utils.rendering import *

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

def detect(frame, camera_matrix, dist_coefs):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame_gray, aruco_dict, parameters=parameters)

    rendered_img = frame
    rvecs = []
    tvecs = []
    if corners != []:
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 8.0, camera_matrix, dist_coefs)
        rvec = rvecs[0]
        tvec = tvecs[0]
        rendered_img = aruco.drawAxis(rendered_img, camera_matrix, dist_coefs, rvec, tvec, 10.0)

    return (rvecs, tvecs, rendered_img)
