"""
    This module contains the registry functions used in OpenGL draw cycle
    * idle: function executed until the threshold detection
    * colorDetection: threshold detection on the current frame
    * loading: code for initializing game and launching players
    * render: code executed during main draw cycle, shows both frame and chessboard
    * systemExit: termination of the application

    * loadBackground: loads background webcam frame in OpenGL window
"""

import threading
import settings as config
import glut_application as glta
import pieces_init as pieces_data

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from threading import Thread
from aruco import *
from thread_p import *
from IA_player import *
from pieces_init import *
from calibration import *
from find_centers import *
from model_utils import *
from human_player import *
from selector_utils import *


playerW = None
playerB = None

def systemExit(args):

    for key in pieces_data.PIECES_POSITION.keys():
        glDeleteLists(pieces_data.PIECES_POSITION[key], 1)

    if playerW != None and playerB != None:
        playerW.terminate()
        playerB.terminate()

    glta.webcam.release()
    glutLeaveMainLoop()


def idle(args):

    img = args[0]

    start_point = (int(img.shape[1]/2), int(img.shape[0]/2))
    end_point = (int(img.shape[1]/2 + 150), int(img.shape[0]/2 + 150))

    cv2.rectangle(img, start_point, end_point, (0,255,0), 2)

    loadBackground(img)


def colorDetection(args):

    img = args[0]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    offset_H = 10
    offset_S = 70

    start_point = (int(img.shape[1]/2), int(img.shape[0]/2))
    end_point = (int(img.shape[1]/2 + 150), int(img.shape[0]/2 + 150))

    sub_image = img[start_point[1]:end_point[1], start_point[0]:end_point[0], :]
    mean = np.mean(sub_image, axis = (0,1))

    low_th = [mean[0]-offset_H, mean[1]-offset_S, 20]
    high_th = [mean[0]+offset_H, mean[1]+offset_S, 255]

    if low_th[0] < 0:
        low_th[0] = 0
    if high_th[0] < 0:
        high_th[0] = 0
    if low_th[0] >180:
        low_th[0] = 180
    if high_th[0] > 180:
        high_th[0] = 180

    if low_th[1] < 0:
        low_th[1] = 0
    if high_th[1] < 0:
        high_th[1] = 0
    if low_th[1] >255:
        low_th[1] = 255
    if high_th[1] > 255:
        high_th[1 ] = 255

    print("THRESHOLDS FOUND:", low_th, high_th)

    config.low_th = low_th
    config.high_th = high_th

    glta.state="LOADING"


def loading(args):
    global playerW, playerB

    _chessboard = Chessboard.getInstance()
    glta.current = _chessboard.getPieces()

    cv2.namedWindow("Chess debug window",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Chess debug window", 350,350)
    cv2.moveWindow("Chess debug window", 0,300);
    cv2.imshow("Chess debug window", _chessboard.toPrint())

    human = HumanPlayer("WHITE")
    ia = IAPlayer("BLACK")
    playerW = Thread_P(human)
    playerB = Thread_P(ia)
    playerW.start()
    playerB.start()

    glta.state="PLAYING"


def render(args):

    img = args[0]
    config.queue_img.put(cv2.cvtColor(img,cv2.COLOR_RGB2BGR))

    _chessboard = Chessboard.getInstance()
    glta.current = _chessboard.getPieces()
    cv2.imshow("Chess debug window", _chessboard.toPrint())

    updateChessboard(glta.current, glta.previous)
    updateSelector()
    rvec, tvec, img = detect(img, config.camera_matrix, config.dist_coefs)
    h, w = img.shape[:2]

    loadBackground(img)

    # Enable / Disable
    glEnable(GL_DEPTH_TEST)     # Enable GL_DEPTH_TEST
    glEnable(GL_LIGHTING)       # Enable Light
    glEnable(GL_LIGHT0)         # Enable Light
    glDisable(GL_TEXTURE_2D)    # Disable texture map

    # Make projection matrix
    m1 = np.array([
    [(glta.alpha)/glta.cx, 0, 0, 0],
    [0, glta.beta/glta.cy, 0, 0],
    [0, 0, -(glta.f+glta.n)/(glta.f-glta.n), (-2.0*glta.f*glta.n)/(glta.f-glta.n)],
    [0,0,-1,0],
    ])
    glLoadMatrixd(m1.T)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()

    # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.0,0.0,1.0,1.0])
    lightfv = ctypes.c_float * 4
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    if len(rvec[0]) != 0 and len(tvec[0]) != 0:
        # Fix axis
        tvec[0][0][0] = tvec[0][0][0]
        tvec[0][0][1] = -tvec[0][0][1]
        tvec[0][0][2] = -tvec[0][0][2]

        rvec[0][0][1] = -rvec[0][0][1]
        rvec[0][0][2] = -rvec[0][0][2]
        m = compositeArray(cv2.Rodrigues(rvec)[0], tvec[0][0])

        glPushMatrix()
        glLoadMatrixd(m.T)
        glta.current_mvm = glGetDoublev(GL_MODELVIEW_MATRIX)

        # glTranslatef(0, 0, -0.5)
        glRotatef(-180, 1.0, 0.0, 0.0)
        glCallList(pieces_data.id_selectionSprite)
        glCallList(pieces_data.id_chessboardList)

        for key in pieces_data.PIECES_POSITION.keys():
            glCallList(pieces_data.PIECES_POSITION[key])

        glPopMatrix()

    glPopMatrix()

    if _chessboard.isEnded():
        glta.state="EXIT"

    glta.previous = glta.current


def loadBackground(img):

    h, w = img.shape[:2]

    glBindTexture(GL_TEXTURE_2D, glta.texture_background)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img)

    # Enable / Disable
    glDisable(GL_DEPTH_TEST)    # Disable GL_DEPTH_TEST
    glDisable(GL_LIGHTING)      # Disable Light
    glDisable(GL_LIGHT0)        # Disable Light
    glEnable(GL_TEXTURE_2D)     # Enable texture map

    # Init
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear Buffer
    glColor3f(1.0, 1.0, 1.0)    # Set texture Color(RGB: 0.0 ~ 1.0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Draw background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, glta.texture_background)
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
