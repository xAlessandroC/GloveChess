import cv2
import numpy as np
import ctypes
import time
import random
import pieces_data as pieces_data
import config as config

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from aruco import *
from calibration import *
from objloader_complete import *
from webcam import *
from opengl_utils import *
from register_functions import *
from findCenters import *
from mouse_interaction import *
from chessboard import *
from executer import *
from piece import *


###############################
# GLOBAL VARIABLES
texture_background = None
chess_piece = None
webcam = None

windowWidth = 1280
windowHeight = 720

f = 1000.0
n = 1.0

alpha = None
beta = None
cx = None
cy = None

_chessboard = None

centers = []
current = []
previous = []

count = 0

obj_s = None
selector_x = 0
selector_y = 0

current_mvm = None
m_old = np.zeros((4,4))
###############################

###############################
## REGISTER
register = {
"IDLE": idle,
"DETECTION": colorDetection,
"LOADING": loading,
"PLAYING": render,
"EXIT": systemExit
}
##############################

def keyboard(key, x, y):
    global selector_x, selector_y, obj_s

    bkey = key.decode("utf-8")
    if bkey == "q":
        config.state="EXIT"
    elif bkey == "d":
        config.state="DETECTION"


def draw():
    global count
    img = webcam.getNextFrame()
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #BGR-->RGB

    register[config.state]([img])

    glFlush();
    glutSwapBuffers()

##############################

###############################
# INIT
def init_param():
    global camera_matrix, alpha, beta, cx, cy, _chessboard, centers, webcam

    alpha = config.camera_matrix[0][0]
    beta = config.camera_matrix[1][1]
    cx = config.camera_matrix[0][2]
    cy = config.camera_matrix[1][2]

    webcam = Webcam(0)

    _chessboard = Chessboard.getInstance()

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
    print("SETTATA TEXTURE: ", texture_background)

###############################
# APPLICATION
def init_application():
    init_param()
    init_piece(centers)
    init_gl()

def init_glContext():
    # glutInitWindowPosition(0, 0);
    # glutInitWindowSize(windowWidth, windowHeight);
    glutInit(sys.argv)

    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS);
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow("AR CHESS")
    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutIdleFunc(draw)

    glutFullScreen()

def start_application():
    glutMainLoop()
