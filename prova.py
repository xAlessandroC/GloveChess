from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import cv2
import numpy as np
import time
from utils.calibration import *
from utils.objloader_complete import *
from utils.paths import *

import ctypes

USE_CAMERA = True

texture_background = None

# Set AR
aruco = cv2.aruco
dictionary = aruco.Dictionary_get(aruco.DICT_6X6_250)

#load camera parameter
mtx, dist, rvecs, tvecs = calibrate()

alpha = mtx[0][0]
beta = mtx[1][1]
cx = mtx[0][2]
cy = mtx[1][2]

chess_piece = None

if USE_CAMERA:
    # USB camera setup
    cap = cv2.VideoCapture(0)
    if cap.isOpened() is False:
        raise("IO Error")
    # cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

windowWidth = 1280
windowHeight = 720

def draw():
    if USE_CAMERA:
        ret, img = cap.read() #read camera image
    else:
        img = cv2.imread('testimg.jpg') # if use the image file

    # Aruco
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, dictionary)
    rvec, tvec, _objPoints = aruco.estimatePoseSingleMarkers(corners, 8.0, mtx, dist)
    if not ids is None:
        # draw axis and center circle
        p1 = corners[0][0][2]
        p2 = corners[0][0][1]
        p3 = corners[0][0][0]
        p4 = corners[0][0][3]
        s1 = ((p4[0] - p2[0])*(p1[1] - p2[1]) - (p4[1] - p2[1])*(p1[0] - p2[0])) / 2
        s2 = ((p4[0] - p2[0])*(p2[1] - p3[1]) - (p4[1] - p2[1])*(p2[0] - p3[0])) / 2
        c1x = p1[0] + (p3[0] - p1[0]) * s1 / (s1 + s2)
        c1y = p1[1] + (p3[1] - p1[1]) * s1 / (s1 + s2)
        cv2.circle(img,(int(c1x), int(c1y)),10,(0,0,1))
        aruco.drawAxis(img, mtx, dist, rvec[0], tvec[0], 8.0)
    img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #BGR-->RGB
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
    f = 1000.0  #far
    n = 1.0     #near

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
    glPushMatrix()  #projection Push(?)

    # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.0,0.0,1.0,1.0])
    lightfv = ctypes.c_float * 4
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    if not ids is None:
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
        drawObj()
        glPopMatrix()

    glPopMatrix()   #projection POP(?)


    glFlush();
    glutSwapBuffers()


def compositeArray(rvec, tvec):
    v = np.c_[rvec, tvec.T]
    #print(v)
    v_ = np.r_[v, np.array([[0,0,0,1]])]
    return v_

def drawObj():
    global chess_piece

    # glutSolidCube(3.0)
    glCallList(chess_piece.gl_list)

def init():
    global chess_piece, texture_background
    #glClearColor(0.7, 0.7, 0.7, 0.7)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    chess_piece = OBJ(obj_path)

    glEnable(GL_TEXTURE_2D)
    texture_background = glGenTextures(1)

def idle():
    glutPostRedisplay()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glLoadIdentity()
    glOrtho(-w / windowWidth, w / windowWidth, -h / windowHeight, h / windowHeight, -1.0, 1.0)

def keyboard(key, x, y):
    # convert byte to str
    key = key.decode('utf-8')
    if key == 'q':
        print('exit')
        sys.exit()

if __name__ == "__main__":
    glutInitWindowPosition(0, 0);
    glutInitWindowSize(windowWidth, windowHeight);
    glutInit(sys.argv)

    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS);
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow(b"Display")
    glutDisplayFunc(draw)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    init()
    glutIdleFunc(idle)

    glutMainLoop()
