import cv2
import numpy as np
import ctypes
import time
import random
import pieces_data as pieces_data
import config as config
import aruco as aruco_config
from queue import *

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


#TODO: pushare risorse nuove
###############################
# GLOBAL VARIABLES
texture_background = None
chess_piece = None
webcam = None

windowWidth = 900
windowHeight = 506

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

current_mvm = None
m_old = np.zeros((4,4))

queue_A = Queue()
queue_B = Queue()
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

    bkey = key.decode("utf-8")
    if bkey == "q":
        config.state="EXIT"
    elif bkey == "d":
        config.state="DETECTION"
    elif bkey == "o":
        if aruco_config.size_marker > 1:
            aruco_config.size_marker = aruco_config.size_marker - 0.5
    elif bkey == "l":
        if aruco_config.size_marker < 14:
            aruco_config.size_marker = aruco_config.size_marker + 0.5

def draw():
    global count
    img = webcam.getNextFrame()

    # Mostro il frame "puro" prima di utilizzarlo per le varie operazioni
    cv2.namedWindow("Debug window",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Debug window", 356,200)
    cv2.imshow("Debug window",img)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

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
    glutIdleFunc(draw)

    glutFullScreen()

def start_application():
    glutMainLoop()
