import numpy as np
import cv2
from cv2 import aruco

from utils.paths import *
from utils.feature_detection import *
from utils.rendering import *

id = 50
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
img = aruco.drawMarker(aruco_dict, id, 200)
cache = None
model = cv2.imread("resources/marker/aruco/model_50.png",0)
h,w = model.shape


def detect(frame, camera_matrix, dist_coefs, obj):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame_gray, aruco_dict, parameters=parameters)
    # frame = aruco.drawDetectedMarkers(frame, corners, ids)

    # src_pts = np.float32([ [0,0],[0,h-1],[w-1,0],[w-1,h-1] ]).reshape(-1,1,2)
    rendered_img = frame
    rvecs = []
    tvecs = []
    projection_m = []
    center = []
    if corners != []:
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 8.0, camera_matrix, dist_coefs)
        rvec = rvecs[0]
        tvec = tvecs[0]
        rendered_img = aruco.drawAxis(rendered_img, camera_matrix, dist_coefs, rvec, tvec, 6.0)

        # c = corners[0][0]
        # center_x = c[:, 0].mean()
        # center_y = c[:, 1].mean()
        # center = [center_x, center_y]

        # rendered_img = cv2.circle(rendered_img,center,5,(255,0,0),20)
        # dst_pts = np.array(corners, dtype="float32").reshape(-1,1,2)
        # M, mask = cv2.findHomography(src_pts, dst_pts)
        # projection_m = projection_matrix(camera_matrix,M)
        # _2d_points = show_axis(rendered_img,projection_m)
        # rendered_img = renderCube(rendered_img, rvec, tvec, camera_matrix, dist_coefs)

    return (rvecs, tvecs, rendered_img, center, projection_m)
