"""
    OpenGL application.
"""

import cv2
import time
import ctypes
import random
import numpy as np
import settings as config
import aruco as aruco_config
import pieces_init as pieces_data

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from queue import *
from aruco import *
from webcam import *
from executer import *
from chess_enum import *
from chessboard_model import *
from calibration import *
from find_centers import *
from opengl_utils import *
from objloader_complete import *
from register_functions import *


#TODO: pushare risorse nuove

# Global variables
texture_background = None

f = 1000.0
n = 1.0
alpha = None
beta = None
cx = None
cy = None

obj_s = None

webcam = None

centers = []
current = []
previous = []

current_mvm = None

state = "IDLE"


# Register
register = {
    "IDLE": idle,
    "DETECTION": colorDetection,
    "LOADING": loading,
    "PLAYING": render,
    "EXIT": systemExit
}


def keyboard(key, x, y):
    global state

    bkey = key.decode("utf-8")

    if bkey == "q":
        state="EXIT"

    elif bkey == "d":
        state="DETECTION"

    elif bkey == "o":
        if aruco_config.size_marker > 1:
            aruco_config.size_marker = aruco_config.size_marker - 0.5

    elif bkey == "l":
        if aruco_config.size_marker < 14:
            aruco_config.size_marker = aruco_config.size_marker + 0.5


def draw():

    img = webcam.getNextFrame()
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    # Apply the right function according to the current state
    register[state]([img])

    glFlush();
    glutSwapBuffers()

##############################

###############################
# Init
def init_param():
    global alpha, beta, cx, cy, centers, webcam

    alpha = config.camera_matrix[0][0]
    beta = config.camera_matrix[1][1]
    cx = config.camera_matrix[0][2]
    cy = config.camera_matrix[1][2]

    webcam = Webcam(0)

    centers = findCenters()
    centers = centers.reshape(8,8,2)
    centers = np.flip(centers,1)
    centers = np.flip(centers,0)


def init_gl():
    global texture_background

    #glClearColor(0.7, 0.7, 0.7, 0.7)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    texture_background = glGenTextures(1)
    print("Texture setting: ", texture_background)


###############################
# Application

def init_application():
    init_param()
    init_piece(centers)
    init_gl()


def init_glContext():
    glutInitWindowPosition(config.init_width_GL, config.init_height_GL);
    glutInitWindowSize(config.width_GL, config.height_GL);
    glutInit(sys.argv)

    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS);
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow("GLOVE CHESS")
    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(draw)

    # glutFullScreen()


def start_application():
    glutMainLoop()
