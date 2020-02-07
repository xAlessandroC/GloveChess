import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import pywavefront
from pywavefront import visualization

from calibration import *
from feature_detection import *
from rendering import *

test_path = "resources/marker/image_1.jpg"
model_path = "resources/marker/model.png"

camera_matrix, dist_coefs, rvecs, tvecs = calibrate()

test_image = cv2.imread(test_path,0)
model_image = cv2.imread(model_path,0)

img, projection_m = detect(test_image,model_image,camera_matrix,0)

dirname = "resources/chess_models/Alfiere_Bianco/"
fn = dirname + "12929_WoodenChessBishopSideA_diffuse.jpg"
obj = pywavefront.Wavefront(dirname + "12929_WoodenChessBishopSideA_v1_l3.obj",create_materials=True,collect_faces=True)

to_render = cv2.cvtColor(cv2.imread(test_path),cv2.COLOR_BGR2RGB)
rendered_img = render(to_render, obj, projection_m)

plt.imshow(rendered_img)
plt.show()
