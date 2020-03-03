import numpy as np
import cv2
import os
from matplotlib import pyplot as plt

square_size = 26.5
pattern_size = (8,5)

def processImage(fn, pattern_points):
    print('processing {}'.format(fn))
    img = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("Failed to load", fn)
        return None

    found, corners = cv2.findChessboardCorners(img, pattern_size)

    if found:
        #Refining corner position to subpixel iteratively until criteria  max_count=30 or criteria_eps_error=1 is sutisfied
        term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 5, 1)
        #Image Corners
        cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

    ##VISUALIZATION
    # vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # cv2.drawChessboardCorners(vis, pattern_size, corners, found)
    #
    # plt.imshow(vis)
    # plt.show()

    if not found:
        print('chessboard not found')
        return None

    print('           %s... OK' % fn)
    return (corners.reshape(-1, 2), pattern_points)

def calibration():

    dirname = "resources/calibration/webcam/"
    img_names = [dirname + str(i) + ".jpg" for i in range(19)]

    indices = np.indices(pattern_size, dtype=np.float32)
    indices *= square_size

    pattern_points = np.zeros([pattern_size[0]*pattern_size[1], 3], np.float32)
    coords_3D = indices.T
    coords_3D = coords_3D.reshape(-1, 2)
    pattern_points[:, :2] = coords_3D

    chessboards = [processImage(fn, pattern_points) for fn in img_names]
    chessboards = [x for x in chessboards if x is not None]

    obj_points = [] #3D points
    img_points = [] #2D points

    for (corners, pattern_points) in chessboards:
            img_points.append(corners)
            obj_points.append(pattern_points)

    h, w = cv2.imread(img_names[0], cv2.IMREAD_GRAYSCALE).shape[:2]

    # Calibrating Camera
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)
    print("Calibrazione completed: RMS =",rms)
    return (rms, camera_matrix, dist_coefs, rvecs, tvecs)


def calibrate():
    parameters_path = "resources/data/"

    ##CACHE CALIBRATION RESULTS
    if len(os.listdir(parameters_path)) != 4:
        print("[Error]: Parameters file not present ", len(os.listdir(parameters_path)))
        rms, camera_matrix, dist_coefs, rvecs, tvecs = calibration()
        np.save(parameters_path+"camera_matrix.npy", camera_matrix)
        np.save(parameters_path+"dist_coefs.npy", dist_coefs)
        np.save(parameters_path+"rvecs.npy", rvecs)
        np.save(parameters_path+"tvecs.npy", tvecs)
    else:
        print("Loading calibration results...")
        camera_matrix = np.load(parameters_path+"camera_matrix.npy")
        dist_coefs = np.load(parameters_path+"dist_coefs.npy")
        rvecs = np.load(parameters_path+"rvecs.npy")
        tvecs = np.load(parameters_path+"tvecs.npy")

    return (camera_matrix,dist_coefs,rvecs,tvecs)
