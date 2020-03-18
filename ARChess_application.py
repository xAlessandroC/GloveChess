from glut_application import *
from utils.calibration import *
import utils.config as config
from pieces_data import *


if __name__ == "__main__":
    print("Starting application...")

    # CAMERA CALIBRATION
    cmtx, dcfs, rvecs, tvecs = calibrate()

    config.camera_matrix = cmtx
    config.dist_coefs = dcfs

    init_application()
    load_pieces()
    init_piece()

    start_application()
