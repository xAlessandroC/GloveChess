import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import pywavefront
from pywavefront import visualization

from calibration import *
from feature_detection import *
from rendering import *


test_path = "resources/marker/image_5.jpg"
model_path = "resources/marker/model.png"
obj_path = "resources/chess_models/Alfiere_Bianco/12929_WoodenChessBishopSideA_v1_l3.obj"
# obj_path = "resources/chess_models/Random/chess.obj"

camera_matrix, dist_coefs, rvecs, tvecs = calibrate()

test_image = cv2.imread(test_path,0)
model_image = cv2.imread(model_path,0)

img, projection_m = detect(test_image,model_image,camera_matrix,1)

# r = 10
# rotate_m = np.asarray([[-r,1,1,1],[-r,1,1,1],[r,1,1,1]])
# projection_m = projection_m * rotate_m

obj = pywavefront.Wavefront(obj_path, create_materials=True,collect_faces=True)

#SWAP
# obj.vertices = list(map(lambda sub: (sub[1], sub[0], sub[2]), obj.vertices))

to_render = cv2.cvtColor(cv2.imread(test_path),cv2.COLOR_BGR2RGB)
_2d_points = show_axis(to_render,projection_m)
rendered_img = render(to_render, obj, projection_m, model_image)

plt.imshow(rendered_img)
for point in _2d_points:
    if point[:,0] <1024 and point[:,1] <1024:
        plt.scatter(point[:,0],point[:,1])
plt.show()
