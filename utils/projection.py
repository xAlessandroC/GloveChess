import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import pywavefront
from pywavefront import visualization

from utils.calibration import *
from utils.feature_detection import *
from utils.rendering import *
from utils.objLoader import *
from utils.paths import *

camera_matrix, dist_coefs, rvecs, tvecs = calibrate()

test_image = cv2.imread(test_path,0)
model_image = cv2.imread(model_path,0)

img, projection_m = detect(test_image,camera_matrix,0)

# obj = pywavefront.Wavefront(obj_path, create_materials=True,collect_faces=True)
obj = OBJ(obj_path, True)

to_render = cv2.cvtColor(cv2.imread(test_path),cv2.COLOR_BGR2RGB)
# _2d_points = show_axis(to_render,projection_m)
rendered_img = render(to_render, obj, projection_m, model_image)

plt.imshow(rendered_img)
# for point in _2d_points:
#     if point[:,0] <1024 and point[:,1] <1024:
#         plt.scatter(point[:,0],point[:,1])
plt.show()
