import cv2
import numpy as np

###############################
# GLOBAL VARIABLES
INVERSE_MATRIX = np.array([[1.0, 1.0, 1.0, 1.0],
                           [-1.0, -1.0, -1.0, -1.0],
                           [-1.0, -1.0, -1.0, -1.0],
                           [1.0, 1.0, 1.0, 1.0]])

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


def getOpenglProjectionMatrix(camera_matrix, near, far, width, height):
    K00 = camera_matrix[0][0]
    K11 = camera_matrix[1][1]
    K01 = camera_matrix[0][1]
    K02 = camera_matrix[0][2]
    K12 = camera_matrix[1][2]


    result = np.zeros((4,4))

    result[0,0] = 2*K00 / width
    result[0,1] = -2*K01 / width
    result[0,2] = (width - 2*K02 + 2*0) / width
    result[0,3] = 0

    result[1,0] = 0
    result[1,1] = -2*K11 / height
    result[1,2] = (height - 2*K12 + 2*0) / height
    result[1,3] = 0

    result[2,0] = 0
    result[2,1] = 0
    result[2,2] = (-far - near) / (far - near)
    result[2,3] = -2*far*near/(far-near)

    result[3,0] = 0
    result[3,1] = 0
    result[3,2] = -1
    result[3,3] = 0

    print(result)
