import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
import time

##Versione per pywavefront
# def render (img, obj, projection_matrix, model):
#
#     vertices = obj.vertices
#     scale_matrix = np.eye(3) * 10
#     h, w = model.shape
#     # rot = getRotationMatrix()
#
#     for face in obj.mesh_list[0].faces:
#         points = np.array([vertices[vertex - 1] for vertex in face)
#         np_3d_points = np.asarray(points).astype(np.float32)
#         np_3d_points = np.dot(np_3d_points, scale_matrix)
#         # np_3d_points = np.dot(np_3d_points, rot)
#         # np_3d_points = np.array([[p[0] + w / 4, p[1] + h / 4, p[2]] for p in np_3d_points])
#         _2d_points = cv2.perspectiveTransform(np_3d_points.reshape(-1, 1, 3), projection_matrix)
#         _2d_points = np.asarray(_2d_points).astype(np.int32)
#         cv2.fillConvexPoly(img, _2d_points, (137, 27, 211))
#
#     return img

##Versione per objLoader
def render (img, obj, projection_matrix, model):

    vertices = obj.vertices
    scale_matrix = np.eye(3) * 2
    h, w = model.shape
    # rot = getRotationMatrix()

    for face in obj.faces:
        points = np.array([vertices[vertex - 1] for vertex in face[0]])
        np_3d_points = np.asarray(points).astype(np.float32)
        np_3d_points = np.dot(np_3d_points, scale_matrix)
        # np_3d_points = np.dot(np_3d_points, rot)
        # np_3d_points = np.array([[p[0] + w / 4, p[1] + h / 4, p[2]] for p in np_3d_points])
        _2d_points = cv2.perspectiveTransform(np_3d_points.reshape(-1, 1, 3), projection_matrix)
        _2d_points = np.asarray(_2d_points).astype(np.int32)
        cv2.fillConvexPoly(img, _2d_points, (137, 27, 211))

    return img

def show_axis (img, projection_matrix):

    axis_1 = np.empty([1,3])
    axis_2 = np.empty([1,3])
    axis_3 = np.empty([1,3])

    for i in range(50):
        axis_1 = np.append(axis_1,[[i,0,0]],axis=0)
        axis_2 = np.append(axis_2,[[0,i,0]],axis=0)
        axis_3 = np.append(axis_3,[[0,0,i]],axis=0)

    np_3d_points = np.concatenate((axis_1,axis_2,axis_3), axis=0)
    np_3d_points = np.asarray(np_3d_points).astype(np.float32)

    _2d_points = cv2.perspectiveTransform(np_3d_points.reshape(-1, 1, 3), projection_matrix)
    _2d_points = np.asarray(_2d_points).astype(np.int32)

    return _2d_points


def getRotationMatrix():
    a = 77
    b = 180
    c = 0
    rot_matrix_X = np.array([[1,0,0],
                           [0,math.cos(a),-math.sin(a)],
                           [0,math.sin(a),math.cos(a)]])
    rot_matrix_Y = np.array([[math.cos(b),0,math.sin(b)],
                           [0,1,0],
                           [-math.sin(b),0,math.cos(b)]])
    rot_matrix_Z = np.array([[math.cos(c),-math.sin(c),0],
                           [math.sin(c),math.cos(c),0],
                           [0,0,1]])
    tot = np.dot(np.dot(rot_matrix_X, rot_matrix_Y),rot_matrix_Z)

    return tot
