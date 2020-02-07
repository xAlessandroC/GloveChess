import numpy as np
import cv2

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

    if not found:
        print('chessboard not found')
        return None

    print('           %s... OK' % fn)
    return (corners.reshape(-1, 2), pattern_points)

def calibrate():

    dirname = "resources/calibration/"
    img_names = [dirname + str(i) + ".jpg" for i in range(13)]

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
    return (rms, camera_matrix, dist_coefs, rvecs, tvecs)
