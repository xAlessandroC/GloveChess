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

    # OPENGL_APP
    start_application()
