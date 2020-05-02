"""
    Authors: Alessandro Calvio
             Alfonso D'Acunzo
             Lorenzo Mustich

    Main app
"""

import sys
sys.path.append('./model/')
sys.path.append('./opengl_application/')
sys.path.append('./aruco_markerdetection/')
sys.path.append('./system_utils/')
sys.path.append('./player/')
sys.path.append('./IA/')
sys.path.append('./human/')

import threading
import settings as config

from glut_application import *
from calibration import *
from pieces_init import *
from player import *

if __name__ == "__main__":
    print("Starting Glove Chess...")

    # CAMERA CALIBRATION
    cmtx, dcfs, rvecs, tvecs = calibrate()

    config.camera_matrix = cmtx
    config.dist_coefs = dcfs

    init_glContext()
    load_pieces()

    init_application()

    # Open debug windows
    cv2.namedWindow("Glove window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Glove window", 356,200)
    cv2.moveWindow("Glove window", 0, 20)

    cv2.namedWindow("Chess debug window",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Chess debug window", 350,350)
    cv2.moveWindow("Chess debug window", 0,280);

    # OPENGL_APP
    start_application()
