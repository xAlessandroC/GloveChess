import sys
sys.path.append('./model/')
sys.path.append('./opengl_application/')
sys.path.append('./aruco_markerdetection/')
sys.path.append('./utils/')
sys.path.append('./player/')
sys.path.append('./IA/')
sys.path.append('./gui/')

import config as config
import threading
from guiVisualizer import *
from calibration import *
from glut_application import *
from pieces_data import *
from player import *

if __name__ == "__main__":
    print("Starting application...")

    # CAMERA CALIBRATION
    cmtx, dcfs, rvecs, tvecs = calibrate()

    config.camera_matrix = cmtx
    config.dist_coefs = dcfs


    init_glContext()
    load_pieces()
    # Thread(target=startGui, args=()).start()

    init_application()

    # OPENGL_APP
    start_application()
