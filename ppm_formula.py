import cv2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

###############################
# GLOBAL VARIABLES
INVERSE_MATRIX = np.array([[1.0, 1.0, 1.0, 1.0],
                           [-1.0, -1.0, -1.0, -1.0],
                           [-1.0, -1.0, -1.0, -1.0],
                           [1.0, 1.0, 1.0, 1.0]])


# INVERSE_MATRIX = np.array([[1.0, 0.0, 0.0, 0.0],
#                            [-0.0, -1.0, -0.0, -0.0],
#                            [-0.0, -0.0, -1.0, -0.0],
#                            [0.0, 0.0, 0.0, 1.0]])

###############################

def getCorrectPPM(rvec,tvec):
    rtmx = cv2.Rodrigues(rvec)[0]

    view_matrix = np.array([[rtmx[0][0],rtmx[0][1],rtmx[0][2],tvec[0,0]],
                            [rtmx[1][0],rtmx[1][1],rtmx[1][2],tvec[0,1]],
                            [rtmx[2][0],rtmx[2][1],rtmx[2][2],tvec[0,2]],
                            [0.0,       0.0,       0.0,       1.0   ]])

    view_matrix = view_matrix * INVERSE_MATRIX
    view_matrix = np.transpose(view_matrix)

    return view_matrix

def tryThis(p_k):
    Rx = np.array([[1,0,0],[0,0,-1],[0,1,0]])
    print(p_k)
    print(p_k.shape)

    # set rotation to best approximation
    R = p_k[:,:3]
    U,S,V = np.linalg.svd(R)
    R = np.dot(U,V)
    R[0,:] = -R[0,:] # change sign of x-axis

    # set translation
    t = p_k[:,3]

    # setup 4*4 model view matrix
    M = np.eye(4)
    M[:3,:3] = np.dot(R,Rx)
    M[:3,3] = t

    # transpose and flatten to get column order
    M = M.T
    m = M.flatten()
    return m


def getOpenglProjectionMatrix(camera_matrix, near, far, width, height):
    K00 = camera_matrix[0][0]
    K11 = camera_matrix[1][1]
    K01 = camera_matrix[0][1]
    K02 = camera_matrix[0][2]
    K12 = camera_matrix[1][2]

    height = 720
    width = 1280

    fx = K00
    fy = K11
    fovy = 2*np.arctan(0.5*height/fy)*180/np.pi
    aspect = (width*fy)/(height*fx)
    near = 0.1
    far = 100.0

    print("FOVY:",fovy)
    print("ASPECT:",aspect)

    result00 = 2*K00 / width
    # result[0,1] = -2*K01 / width
    result01 = 0
    result02 = (width - 2*K02 + 2*0) / width
    result03 = 0

    result10 = 0
    result11 = -2*K11 / height
    result12 = (height - 2*K12 + 2*0) / height
    result13 = 0

    result20 = 0
    result21 = 0
    result22 = (-far - near) / (far - near)
    result23 = -2*far*near/(far-near)

    result30 = 0
    result31 = 0
    result32 = -1
    result33 = 0

    result = np.array([[result00,result01,result02,result03],
                        [result10,result11,result12,result13],
                        [result20,result21,result22,result23],
                        [result30,result31,result32,result33]])

    print(result)
    print(type(result))

    m = map(float,result.T.flat)
    m = (GLfloat * 16)(*m)

    return m
