from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import cv2
import numpy as np
import time
from utils.calibration import *
from utils.objloader_complete import *
import utils.config as config
from utils.webcam import *
from aruco_markerdetection.aruco import *
from utils.utility import *
from findCenters import *

import ctypes

###############################
# GLOBAL VARIABLES
texture_background = None
chess_piece = None
webcam = Webcam(0)

windowWidth = 1280
windowHeight = 720

f = 1000.0
n = 1.0

# camera_matrix, dist_coefs, rvecs, tvecs = calibrate()

alpha = None
beta = None
cx = None
cy = None

models = []
num = 1
###############################
def keyboard(key, x, y):
    sys.exit()

def draw():
    img = webcam.getNextFrame()

    rvec, tvec, img, center, p_k = detect(img, config.camera_matrix, config.dist_coefs, chess_piece)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #BGR-->RGB
    h, w = img.shape[:2]

    global texture_background
    glBindTexture(GL_TEXTURE_2D, texture_background)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)

    ## Enable / Disable
    glDisable(GL_DEPTH_TEST)    # Disable GL_DEPTH_TEST
    glDisable(GL_LIGHTING)      # Disable Light
    glDisable(GL_LIGHT0)        # Disable Light
    glEnable(GL_TEXTURE_2D)     # Enable texture map

    ## init
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear Buffer
    glColor3f(1.0, 1.0, 1.0)    # Set texture Color(RGB: 0.0 ~ 1.0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    ## draw background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, texture_background)
    glPushMatrix()
    glBegin(GL_QUADS)
    glTexCoord2d(0.0, 1.0)
    glVertex3d(-1.0, -1.0,  0)
    glTexCoord2d(1.0, 1.0)
    glVertex3d( 1.0, -1.0,  0)
    glTexCoord2d(1.0, 0.0)
    glVertex3d( 1.0,  1.0,  0)
    glTexCoord2d(0.0, 0.0)
    glVertex3d(-1.0,  1.0,  0)
    glEnd()
    glPopMatrix()

    ## Enable / Disable
    glEnable(GL_DEPTH_TEST)     # Enable GL_DEPTH_TEST
    glEnable(GL_LIGHTING)       # Enable Light
    glEnable(GL_LIGHT0)         # Enable Light
    glDisable(GL_TEXTURE_2D)    # Disable texture map

    ## make projection matrix
    m1 = np.array([
    [(alpha)/cx, 0, 0, 0],
    [0, beta/cy, 0, 0],
    [0, 0, -(f+n)/(f-n), (-2.0*f*n)/(f-n)],
    [0,0,-1,0],
    ])
    glLoadMatrixd(m1.T)

    ## draw cube
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()

    # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.0,0.0,1.0,1.0])
    lightfv = ctypes.c_float * 4
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    if len(rvec) != 0:
        # fix axis
        tvec[0][0][0] = tvec[0][0][0]
        tvec[0][0][1] = -tvec[0][0][1]
        tvec[0][0][2] = -tvec[0][0][2]

        rvec[0][0][1] = -rvec[0][0][1]
        rvec[0][0][2] = -rvec[0][0][2]
        m = compositeArray(cv2.Rodrigues(rvec)[0], tvec[0][0])
        glPushMatrix()
        glLoadMatrixd(m.T)

        glTranslatef(0, 0, -0.5)
        glRotatef(-180, 1.0, 0.0, 0.0)
        glCallList(chess_piece.gl_list)
        for i in range(num):
            glCallList(models[i].gl_list)
        glPopMatrix()

    glPopMatrix()

    glFlush();
    glutSwapBuffers()

###############################
# INIT
def initParam():
    global camera_matrix, alpha, beta, cx, cy

    alpha = config.camera_matrix[0][0]
    beta = config.camera_matrix[1][1]
    cx = config.camera_matrix[0][2]
    cy = config.camera_matrix[1][2]

def init():
    global chess_piece, texture_background, chess_piece2, cubes
    #glClearColor(0.7, 0.7, 0.7, 0.7)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    centers = findCenters()

    chess_piece = OBJ(config.obj_path)
    for i in range(num):
        models.append(OBJ(config.obj_path2,translation=tuple(centers[i+12])))

    glEnable(GL_TEXTURE_2D)
    texture_background = glGenTextures(1)

###############################
# APPLICATION
def start_application():
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
    initParam()
    init()

    glutMainLoop()
