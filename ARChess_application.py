import sys
sys.path.append('./model/')
sys.path.append('./opengl_application/')
sys.path.append('./aruco_markerdetection/')
sys.path.append('./utils/')

import config as config
from calibration import *
from glut_application import *
from pieces_data import *


if __name__ == "__main__":
    print("Starting application...")

    # CAMERA CALIBRATION
    cmtx, dcfs, rvecs, tvecs = calibrate()

    config.camera_matrix = cmtx
    config.dist_coefs = dcfs

    init_glContext()
    load_pieces()

    init_application()
    start_application()
