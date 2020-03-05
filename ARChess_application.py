from glut_application import *
from utils.calibration import *
import utils.config as config


if __name__ == "__main__":
    print("Starting application...")

    # CAMERA CALIBRATION
    cmtx, dcfs, rvecs, tvecs = calibrate()

    config.camera_matrix = cmtx
    config.dist_coefs = dcfs

    start_application()
