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

frames = getFrames(video_path)
# obj = pywavefront.Wavefront(obj_path, create_materials=True,collect_faces=True)
obj = OBJ(obj_path)

for frame in frames:
    test_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    img, projection_m = detect(test_image,camera_matrix,0)
    # to_render = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    start = time.time()
    rendered_img = render(frame, obj, projection_m, model_image)
    end = time.time()
    print("Rendering time: ", end-start)
    cv2.imshow("",rendered_img)
    if cv2.waitKey(1) == ord('q'):
        break
