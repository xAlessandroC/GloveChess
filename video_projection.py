import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import pywavefront
from pywavefront import visualization

from calibration import *
from feature_detection import *
from rendering import *
from video import *


test_path = "resources/marker/image_1.jpg"
video_path = "resources/marker/videooh_2.mp4"
model_path = "resources/marker/model.png"
obj_path = "resources/chess_models/Alfiere_Bianco/12929_WoodenChessBishopSideA_v1_l3.obj"

camera_matrix, dist_coefs, rvecs, tvecs = calibrate()

frames = getFrames(video_path)
model_image = cv2.imread(model_path,0)
obj = pywavefront.Wavefront(obj_path, create_materials=True,collect_faces=True)

for frame in frames:
    test_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    img, projection_m = detect(test_image,model_image,camera_matrix,0)
    to_render = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    rendered_img = render(to_render, obj, projection_m, model_image)
    cv2.imshow("",rendered_img)
    if cv2.waitKey(1) == ord('q'):
        break
