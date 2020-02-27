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


id = 50
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
img = aruco.drawMarker(aruco_dict, id, 200)
cache = None

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

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # toprint = cv2.cvtColor(cv2.imread("resources/marker/aruco/image_1_m50.jpg"), cv2.COLOR_BGR2RGB)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame_gray, aruco_dict, parameters=parameters)
    frame = aruco.drawDetectedMarkers(frame, corners, ids)

    # print(corners)
    # print(type(corners))
    model = cv2.imread("resources/marker/aruco/model_50.png",0)
    h,w = model.shape
    src_pts = np.float32([ [0,0],[0,h-1],[w-1,0],[w-1,h-1] ]).reshape(-1,1,2)
    rendered_img = frame
    if corners != []:
        rvect, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_coefs)
        rvec = rvecs[0]
        tvec = tvecs[0]
        rendered_img = aruco.drawAxis(rendered_img, camera_matrix, dist_coefs, rvec, tvec, 0.03)

        dst_pts = np.array(corners, dtype="float32").reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts)
        projection_m = projection_matrix(camera_matrix,M)
        # rendered_img = render(frame, obj, projection_m, frame)


    cv2.imshow("",rendered_img)
    if cv2.waitKey(1) == ord('q'):
        break


# img2 = cv2.cvtColor(cv2.imread("resources/marker/image_2.jpg"), cv2.COLOR_BGR2RGB)
plt.imshow(img2)
plt.show()
