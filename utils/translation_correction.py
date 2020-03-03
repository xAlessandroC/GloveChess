import cv2
import numpy as np
import os
from utils.objLoader import *
from utils.paths import *


chess_piece = OBJ("resources/chess_models/Alfiere_Bianco/12929_WoodenChessBishopSideA_v1_l3.obj")
np_vertices = np.asarray(chess_piece.vertices).astype(np.float32)
mean = np.mean(np_vertices,axis=0)
print(mean)

f = open("temp/translated_v.txt", "w")
to_write = ""
scaleFactor = 0.003

for vertex in np_vertices:
    old_first = vertex[0]
    old_second = vertex[1]

    ##TRANSLATION
    new_first = old_first - mean[0]
    new_second = old_second - mean[1]

    ##SCALING
    new_first = new_first * scaleFactor
    new_second = new_second * scaleFactor
    vertex[2] = vertex[2] * scaleFactor

    to_write = to_write + "v" + " " + str(new_first) + " " + str(new_second) + " " + str(vertex[2]) + "\n"
    # print("v",new_first, new_second, vertex[2])

f.write(to_write)
f.close()
