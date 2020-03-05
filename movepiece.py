import cv2
import numpy as np
import os
from utils.paths import *

# def translate_prova(x,y):
#
#     piece = OBJ("resources/chess_models/Cube/cube.obj")
#     np_vertices = np.asarray(piece.vertices).astype(np.float32)
#     mean = np.mean(np_vertices,axis=0)
#
#     center1 = np.array([mean[0],mean[1]])
#     center2 = np.array([x,y]).astype(np.float32)
#
#     print(center1)
#     print(center2)
#
#     dist = np.linalg.norm(center1-center2)
#
#     print(dist)
#
#     f = open("temp/translated_v.txt", "w")
#     to_write = ""
#     for vertex in np_vertices:
#         old_first = vertex[0]
#         old_second = vertex[1]
#
#         ##TRANSLATION
#         new_first = old_first + x
#         new_second = old_second + y
#
#         to_write = to_write + "v" + " " + str(new_first) + " " + str(new_second) + " " + str(vertex[2]) + "\n"
#         # print("v",new_first, new_second, vertex[2])
#
#     f.write(to_write)
#     f.close()

def translate(vertices, x, y):

    np_vertices = np.asarray(vertices).astype(np.float32)

    res = []
    for vertex in np_vertices:
        old_first = vertex[0]
        old_second = vertex[1]

        ##TRANSLATION
        new_first = old_first + x
        new_second = old_second + y

        res.append([new_first,new_second,vertex[2]])

    res = np.array(res).astype(np.float32)
    return res
