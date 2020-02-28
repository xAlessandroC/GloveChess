import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
import time

##Versione per objLoader
def render (img, obj, projection_matrix, model, center=[0,0]):

    vertices = obj.vertices
    scale_matrix = np.eye(3) * 10
    # h, w = model.shape
    rot = getRotationMatrix()

    for face in obj.faces:
        points = np.array([vertices[vertex - 1] for vertex in face[0]])
        np_3d_points = np.asarray(points).astype(np.float32)
        # np_3d_points = np.dot(np_3d_points, scale_matrix)
        # np_3d_points = np.dot(np_3d_points, rot)
        # np_3d_points = np.array([[p[0] + center[0], p[1] + center[1], p[2]] for p in np_3d_points])
        _2d_points = cv2.perspectiveTransform(np_3d_points.reshape(-1, 1, 3), projection_matrix)
        _2d_points = np.asarray(_2d_points).astype(np.int32)
        # _2d_points = np.array([[p[0,0] + center[0], p[0,1] + center[1]] for p in _2d_points])
        cv2.fillConvexPoly(img, _2d_points, (255, 0, 0))

    return img

def renderObj(img, obj, rvec, tvec, camera_matrix, dist_coefs):
    vertices = np.array(obj.vertices).astype(np.float32)
    scale_matrix = np.eye(3) * 0.003
    vertices = np.dot(vertices, scale_matrix)
    print("3D:",vertices[0])

    obj_corners_2d, _ = cv2.projectPoints(vertices,rvec,tvec,camera_matrix,dist_coefs)
    # print(cube_corners_2d[0])
    print("2D:",obj_corners_2d[0])

    for face in obj.faces:
        points = np.array([obj_corners_2d[vertex - 1] for vertex in face[0]])
        points = np.asarray(points).astype(np.int32)
        cv2.fillConvexPoly(img, points, (255, 0, 0))

    return img

def renderCube(img, rvec, tvec, camera_matrix, dist_coefs):
    l = 0.07
    _3d_corners = np.float32([[0,0,0], [0,l,0], [l,l,0], [l,0,0], [0,0,l], [0,l,l], [l,l,l], [l,0,l]])
    cube_corners_2d,_ = cv2.projectPoints(_3d_corners,rvec,tvec,camera_matrix,dist_coefs)
    red = (0,0,255) #red (in BGR)
    blue = (255,0,0) #blue (in BGR)
    green = (0,255,0) #green (in BGR)
    black = (0,0,0)
    c1 = (100,100,100)
    c2 = (200,200,200)
    c3 = (77,77,100)
    c4 = (200,100,125)
    c5 = (100,200,77)
    c6 = (125,100,200)
    line_width = 10

    # print(cube_corners_2d)
    # print(type(cube_corners_2d))
    # print(cube_corners_2d.dtype)

    face_1 = np.array([cube_corners_2d[0][0], cube_corners_2d[1][0], cube_corners_2d[2][0], cube_corners_2d[3][0]]).astype(np.int32)
    face_2 = np.array([cube_corners_2d[4][0], cube_corners_2d[5][0], cube_corners_2d[6][0], cube_corners_2d[7][0]]).astype(np.int32)
    face_3 = np.array([cube_corners_2d[0][0], cube_corners_2d[1][0], cube_corners_2d[5][0], cube_corners_2d[4][0]]).astype(np.int32)
    face_4 = np.array([cube_corners_2d[1][0], cube_corners_2d[2][0], cube_corners_2d[6][0], cube_corners_2d[5][0]]).astype(np.int32)
    face_5 = np.array([cube_corners_2d[2][0], cube_corners_2d[3][0], cube_corners_2d[7][0], cube_corners_2d[6][0]]).astype(np.int32)
    face_6 = np.array([cube_corners_2d[3][0], cube_corners_2d[0][0], cube_corners_2d[4][0], cube_corners_2d[7][0]]).astype(np.int32)


    cv2.fillConvexPoly(img, face_1, c1)
    cv2.fillConvexPoly(img, face_2, c2)
    cv2.fillConvexPoly(img, face_3, c3)
    cv2.fillConvexPoly(img, face_4, c4)
    cv2.fillConvexPoly(img, face_5, c5)
    cv2.fillConvexPoly(img, face_6, c6)

    #first draw the base in red
    cv2.line(img, tuple(cube_corners_2d[0][0]), tuple(cube_corners_2d[1][0]),black,line_width)
    cv2.line(img, tuple(cube_corners_2d[1][0]), tuple(cube_corners_2d[2][0]),black,line_width)
    cv2.line(img, tuple(cube_corners_2d[2][0]), tuple(cube_corners_2d[3][0]),black,line_width)
    cv2.line(img, tuple(cube_corners_2d[3][0]), tuple(cube_corners_2d[0][0]),black,line_width)

    #now draw the pillars
    cv2.line(img, tuple(cube_corners_2d[0][0]), tuple(cube_corners_2d[4][0]),black,line_width)
    cv2.line(img, tuple(cube_corners_2d[1][0]), tuple(cube_corners_2d[5][0]),black,line_width)
    cv2.line(img, tuple(cube_corners_2d[2][0]), tuple(cube_corners_2d[6][0]),black,line_width)
    cv2.line(img, tuple(cube_corners_2d[3][0]), tuple(cube_corners_2d[7][0]),black,line_width)

    #finally draw the top
    cv2.line(img, tuple(cube_corners_2d[4][0]), tuple(cube_corners_2d[5][0]),black,line_width)
    cv2.line(img, tuple(cube_corners_2d[5][0]), tuple(cube_corners_2d[6][0]),black,line_width)
    cv2.line(img, tuple(cube_corners_2d[6][0]), tuple(cube_corners_2d[7][0]),black,line_width)
    cv2.line(img, tuple(cube_corners_2d[7][0]), tuple(cube_corners_2d[4][0]),black,line_width)


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
    a = math.radians(90)        ##Piano del tavolo
    b = math.radians(150)
    c = math.radians(120)
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
