import sys
sys.path.append('./model/')
sys.path.append('./opengl_application/')
sys.path.append('./aruco_markerdetection/')
sys.path.append('./utils/')
sys.path.append('./player/')

import config as config
import threading
from calibration import *
from glut_application import *
from pieces_data import *
from player import *

_chessboard = Chessboard.getInstance()
lock = threading.Lock()
condition = threading.Condition(lock)
termination = False

if __name__ == "__main__":
    print("Starting application...")

    # CAMERA CALIBRATION
    cmtx, dcfs, rvecs, tvecs = calibrate()

    config.camera_matrix = cmtx
    config.dist_coefs = dcfs

    init_glContext()
    load_pieces()

    init_application()

    # PLAYERS
    playerW = Player("WHITE")
    playerB = Player("BLACK")

    playerW.start()
    playerB.start()

    # OPENGL_APP
    start_application()

    # Chiusura Threads
    termination = True

    playerW.terminate()
    playerB.terminate()
