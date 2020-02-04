import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
from objloader import *
from rendering import *

def processImage(fn):
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

dirname = "resources/calibration/"
img_names = [dirname + str(i) + ".jpg" for i in range(13)]
print(img_names)

square_size = 26.5
pattern_size = (8,5)
indices = np.indices(pattern_size, dtype=np.float32)
indices *= square_size

pattern_points = np.zeros([pattern_size[0]*pattern_size[1], 3], np.float32)
coords_3D = indices.T
coords_3D = coords_3D.reshape(-1, 2)
pattern_points[:, :2] = coords_3D

chessboards = [processImage(fn) for fn in img_names]
chessboards = [x for x in chessboards if x is not None]

obj_points = [] #3D points
img_points = [] #2D points

for (corners, pattern_points) in chessboards:
        img_points.append(corners)
        obj_points.append(pattern_points)

h, w = cv2.imread(img_names[0], cv2.IMREAD_GRAYSCALE).shape[:2]

# Calibrating Camera
rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)

#print("RMS: ",rms)
#print("CAMERA MATRIX: ",camera_matrix)
#print("DIST_COEFS: ", dist_coefs)
#print("RVECS: ", rvecs)
#print("TVECS: ", tvecs)

test_image = cv2.cvtColor(cv2.imread("resources/calibration/0.jpg"),cv2.COLOR_BGR2RGB)
dir_name = os.getcwd()
obj = OBJ(os.path.join(dir_name, 'resources/chess_models/Alfiere_Bianco/12929_WoodenChessBishopSideA_v1_l3.obj'), swapyz=True)

#print("VERTICES: ", obj.vertices)
#print("NORMAL: ", obj.normals)
#print("TEXT_COORD: ", obj.texcoords)
#print("FACES: ",obj.faces)

#np_3d_points = np.asarray(obj.vertices).astype(np.float32)
#_2d_points = cv2.projectPoints(np_3d_points,rvecs[0],tvecs[0],camera_matrix,dist_coefs)
#print(type(_2d_points))

#cv2.fillConvexPoly(test_image,np.asarray(_2d_points).astype(np.int32),(137, 27, 211))

vertices = obj.vertices
scale_matrix = np.eye(3) * -8
for face in obj.faces:
    face_vertices = face[0]
    points = np.array([vertices[vertex - 1] for vertex in face_vertices])
    np_3d_points = np.asarray(points).astype(np.float32)
    np_3d_points = np.dot(np_3d_points, scale_matrix)
    _2d_points,_ = cv2.projectPoints(np_3d_points,rvecs[0],tvecs[0],camera_matrix,dist_coefs)
    print("ciaociao:",face[-1])
    color = hex_to_rgb(face[-1])
    color = color[::-1]  # reverse
    cv2.fillConvexPoly(test_image, np.asarray(_2d_points).astype(np.int32), color)
    break;

plt.imshow(test_image)
plt.show()
