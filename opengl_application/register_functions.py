from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import config as config
import pieces_data as pieces_data
import glut_application as glta

import guanto_segm
from pieces_data import *
from calibration import *
from findCenters import *
from aruco import *

def idle(args):
    img = args[0]

    start_point = (700, 300)
    end_point = (850, 450)

    cv2.rectangle(img, start_point, end_point, (0,255,0), 2)

    loadBackground(img)

def systemExit(args):
    for key in pieces_data.PIECES_POSITION.keys():
        glDeleteLists(pieces_data.PIECES_POSITION[key], 1)

    glta.webcam.release()
    glutLeaveMainLoop()


def colorDetection(args):
    img = args[0]

    offset_H = 10
    offset_S = 70

    start_point = (700, 300)
    end_point = (850, 450)

    sub_image = img[start_point[1]:end_point[1], start_point[0]:end_point[0], :]
    mean = np.mean(sub_image, axis = (0,1))

    print(offset_S, offset_H)
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

    config.state="LOADING"

def loading(args):

    glta._chessboard = Chessboard.getInstance()

    c = findCenters()
    c = c.reshape(8,8,2)
    c = np.flip(c,1)
    c = np.flip(c,0)
    glta.centers = c

    # TODO: Thread??
    init_piece(glta.centers)

    glta.current = glta._chessboard.getPieces()

    # TODO: Caricamento giocatori

    config.state="PLAYING"

def render(args):
    global texture_background
    updateChessboard(glta.current, glta.previous)

    img = args[0]
    current = glta._chessboard.getPieces()
    rvec, tvec, img = detect(img, config.camera_matrix, config.dist_coefs)
    h, w = img.shape[:2]

    loadBackground(img)

    ## Enable / Disable
    glEnable(GL_DEPTH_TEST)     # Enable GL_DEPTH_TEST
    glEnable(GL_LIGHTING)       # Enable Light
    glEnable(GL_LIGHT0)         # Enable Light
    glDisable(GL_TEXTURE_2D)    # Disable texture map

    ## make projection matrix
    m1 = np.array([
    [(glta.alpha)/glta.cx, 0, 0, 0],
    [0, glta.beta/glta.cy, 0, 0],
    [0, 0, -(glta.f+glta.n)/(glta.f-glta.n), (-2.0*glta.f*glta.n)/(glta.f-glta.n)],
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
        # stabilizza
        m = matrixStabilizer(m, glta.m_old) ##NN

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
        glta.m_old = m.copy()

    glPopMatrix()

    glta.previous = current

def loadBackground(img):
    h, w = img.shape[:2]

    glBindTexture(GL_TEXTURE_2D, glta.texture_background)
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
