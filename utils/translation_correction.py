import cv2
import numpy as np
import os
from utils.objLoader_simple import *
import utils.config as config


chess_piece = OBJ(config.obj_path)
np_vertices = np.asarray(chess_piece.vertices).astype(np.float32)
mean = np.mean(np_vertices,axis=0)
print(mean)
