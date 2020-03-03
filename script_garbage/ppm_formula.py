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
#                            [0.0, -1.0, 0.0, 0.0],
#                            [0.0, 0.0, -1.0, 0.0],
#                            [0.0, 0.0, 0.0, 1.0]])

###############################

def getCorrectPPM(rvec,tvec):
    rvec[0,0] = rvec[0,0]; rvec[0,1] = -rvec[0,1]; rvec[0,2]=-rvec[0,2]

    rtmx = cv2.Rodrigues(rvec)[0]

    view_matrix = np.array([[rtmx[0][0],rtmx[0][1],rtmx[0][2],tvec[0,0]],
                            [rtmx[1][0],rtmx[1][1],rtmx[1][2],-tvec[0,1]],
                            [rtmx[2][0],rtmx[2][1],rtmx[2][2],-tvec[0,2]],
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
    K00 = camera_matrix[0,0]
    K11 = camera_matrix[1,1]
    # K01 = camera_matrix[0,1]
    K02 = camera_matrix[0,2]
    K12 = camera_matrix[1,2]

    width = 1280
    height = 720

    fx = K00
    fy = K11
    fovy = 2*np.arctan(0.5*height/fy)*180/np.pi
    aspect = (width*fy)/(height*fx)

    print("FOVY:",fovy)
    print("ASPECT:",aspect)
    #
    # result = np.array([
    #     [(K00)/K02, 0,       0,            0               ],
    #     [0,          K11/K12, 0,            0               ],
    #     [0,          0,       -(far+near)/(far-near), (-2.0*far*near)/(far-near)],
    #     [0,          0,       -1,           0               ],
    # ])

    # result00 = 2*K00 / width;  result01 = 0; result02 = (width - 2*K02 + 2*0) / width; result03 = 0
    #
    # result10 = 0; result11 = -2*K11 / height; result12 = (height - 2*K12 + 2*0) / height; result13 = 0
    #
    # result20 = 0; result21 = 0; result22 = (-far - near) / (far - near); result23 = -2.0*far*near/(far-near)
    #
    # result30 = 0; result31 = 0; result32 = -1; result33 = 0

    # result00 = 2*K00 / width;  result01 = 0; result02 = 0; result03 = 0
    #
    # result10 = 0; result11 = -2*K11 / height; result12 = 0; result13 = 0
    #
    # result20 = 0; result21 = 0; result22 = (far + near) / (near - far); result23 = -2.0*far*near/(near-far)
    #
    # result30 = 0; result31 = 0; result32 = -1; result33 = 0

    # result = np.array([[result00,result01,result02,result03],
    #                     [result10,result11,result12,result13],
    #                     [result20,result21,result22,result23],
    #                     [result30,result31,result32,result33]])

    result = np.array([
    [(K00)/K02, 0, 0, 0],
    [0, K11/K12, 0, 0],
    [0, 0, -(far+near)/(far-near), (-2.0*far*near)/(far-near)],
    [0,0,-1,0],
    ])

    m = result
    # m = m.T
    # m = map(float,result.T.flat)
    # m = (GLfloat * 16)(*m)

    return m

def getPPM_1(rvec, tvec):
    rot, jacob = cv2.Rodrigues(rvec);

    para = np.empty((3,4))
    para[0][0] = rot[0][0]; para[0][1] = rot[0][1]; para[0][2] = rot[0][0]
    para[1][0] = rot[1][0]; para[1][1] = rot[1][1]; para[1][2] = rot[1][2]
    para[2][0] = rot[2][0]; para[2][1] = rot[2][1]; para[2][2] = rot[2][2]
    para[0][3] = tvec[0][0]; para[1][3] = tvec[0][1]; para[2][3] = tvec[0][1]

    res = np.empty((4,4))
    res[0][0] = para[0][0]; res[0][1] = para[0][1]; res[0][2] = para[0][2]; res[0][3] = para[0][3];
    res[1][0] = para[1][0]; res[1][1] = para[1][1]; res[1][2] = para[1][2]; res[1][3] = para[1][3];
    res[2][0] = -para[2][0]; res[2][1] = -para[2][1]; res[2][3] = -para[2][2]; res[3][3] = -para[2][3];
    res[3][0] = 0; res[3][1] = 0; res[3][2] = 0; res[3][3] = 1;

    res = np.transpose(res)

    return res

def getPPM_2(rvec, tvec):
    tvec[0][0] = tvec[0][0]
    tvec[0][1] = -tvec[0][1]
    tvec[0][2] = -tvec[0][2]

    rvec[0][1] = -rvec[0][1]
    rvec[0][2] = -rvec[0][2]
    m = compositeArray(cv2.Rodrigues(rvec)[0], tvec[0])

    m = m * INVERSE_MATRIX

    return m

def compositeArray(rvec, tvec):
    v = np.c_[rvec, tvec.T]
    #print(v)
    v_ = np.r_[v, np.array([[0,0,0,1]])]
    return v_
