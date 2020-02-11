import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import pywavefront
from pywavefront import visualization
import time

from calibration import *
from feature_detection import *
from rendering import *
from video import *
from paths import *
from objLoader import *

camera_matrix, dist_coefs, rvecs, tvecs = calibrate()

# obj = pywavefront.Wavefront(obj_path, create_materials=True,collect_faces=True)
obj = OBJ(obj_path)
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()

    if not ret or frame is None:
        # Release the Video if ret is false
        cap.release()
        print("Released Video Resource")
        break

    test_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    img, projection_m = detect(test_image,camera_matrix,0)
    # to_render = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    start = time.time()
    rendered_img = render(frame, obj, projection_m, model_image)
    end = time.time()
    print("Rendering time: ", end-start)
    start = time.time()
    cv2.imshow("",rendered_img)
    if cv2.waitKey(1) == ord('q'):
        break
    end = time.time()
    print("Showing time: ", end-start)
