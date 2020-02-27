import cv2
import numpy as np
import os
from utils.objLoader import *
from utils.paths import *


chess_piece = OBJ(obj_path)
np_vertices = np.asarray(chess_piece.vertices).astype(np.float32)
mean = np.mean(np_vertices,axis=0)
print(mean)

f = open("temp/translated_v.txt", "w")
to_write = ""

for vertex in np_vertices:
    old_first = vertex[0]
    old_second = vertex[1]

    new_first = old_first - mean[0]
    new_second = old_second - mean[1]

    to_write = to_write + "v" + " " + str(new_first) + " " + str(new_second) + " " + str(vertex[2]) + "\n"
    # print("v",new_first, new_second, vertex[2])

f.write(to_write)
f.close()
