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
from utility import *
from opengl_utils import *
from findCenters import *
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
###############################
def mouse(button, state, x, y):
    global obj_s
    x_ndc = (2.0 * x + 1.0) / 1280 - 1.0
    y_ndc = (2.0 * y + 1.0) / 720 - 1.0

    modelMatrix_r = glGetDoublev(GL_MODELVIEW_MATRIX)
    projMatrix_r = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport_r = glGetIntegerv(GL_VIEWPORT)

    # print(modelMatrix_r)
    # print(projMatrix_r)
    # print(viewport_r)

    if state == GLUT_DOWN:
        z_value = glReadPixels( x, 720-y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        world_coord = gluUnProject(x, 720-y, z_value, current_mvm, projMatrix_r, viewport_r)
        world_coord = (world_coord[0], -world_coord[1], -world_coord[2])

        center_idx = nearestCenter(centers, *world_coord)
        new_vertices = translateVertices(pieces_data.id_selectionSprite, obj_s, *tuple(centers[center_idx[0], center_idx[1]]), z=13)
        overwriteList(pieces_data.id_selectionSprite, obj_s, new_vertices)
        print("CENTER_IDX:", center_idx)

        print("MVM:",current_mvm)
        print("[VIEWPORT]: Button click at ",x,y)
        print("Z-VALUE:", z_value)
        print("3D COORD:", world_coord)
        # print("[NDC]: Button click at ",x_ndc,y_ndc)


def keyboard(key, x, y):
    global selector_x, selector_y, obj_s

    bkey = key.decode("utf-8")
    # print("KEY:", bkey)
    if bkey == "q":
        for key in pieces_data.PIECES_POSITION.keys():
            glDeleteLists(pieces_data.PIECES_POSITION[key], 1)

        webcam.release()
        glutLeaveMainLoop()
    elif bkey == "w":
        if selector_y < 7:
            selector_y = selector_y + 1
        new_vertices = translateVertices(pieces_data.id_selectionSprite, obj_s, *tuple(centers[selector_x,selector_y]), z=13)
        overwriteList(pieces_data.id_selectionSprite, obj_s, new_vertices)
    elif bkey == "a":
        if selector_x > 0:
            selector_x = selector_x - 1
        new_vertices = translateVertices(pieces_data.id_selectionSprite, obj_s, *tuple(centers[selector_x,selector_y]), z=13)
        overwriteList(pieces_data.id_selectionSprite, obj_s, new_vertices)
    elif bkey == "s":
        if selector_y > 0:
            selector_y = selector_y - 1
        new_vertices = translateVertices(pieces_data.id_selectionSprite, obj_s, *tuple(centers[selector_x,selector_y]), z=13)
        overwriteList(pieces_data.id_selectionSprite, obj_s, new_vertices)
    elif bkey == "d":
        if selector_x < 7:
            selector_x = selector_x + 1
        new_vertices = translateVertices(pieces_data.id_selectionSprite, obj_s, *tuple(centers[selector_x,selector_y]), z=13)
        overwriteList(pieces_data.id_selectionSprite, obj_s, new_vertices)

    # print("Selector in :", selector_x,selector_y)

def draw():
    global previous, current, count, current_mvm

    img = webcam.getNextFrame()
    current = _chessboard.getPieces()

    updateChessboard(current, previous)

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
        count = count + 1
        # fix axis
        tvec[0][0][0] = tvec[0][0][0]
        tvec[0][0][1] = -tvec[0][0][1]
        tvec[0][0][2] = -tvec[0][0][2]

        rvec[0][0][1] = -rvec[0][0][1]
        rvec[0][0][2] = -rvec[0][0][2]
        m = compositeArray(cv2.Rodrigues(rvec)[0], tvec[0][0])
        glPushMatrix()
        glLoadMatrixd(m.T)
        current_mvm = glGetDoublev(GL_MODELVIEW_MATRIX)

        # glTranslatef(0, 0, -0.5)
        glRotatef(-180, 1.0, 0.0, 0.0)
        glCallList(pieces_data.id_selectionSprite)
        glCallList(pieces_data.id_chessboardList)

        for key in pieces_data.PIECES_POSITION.keys():
            glCallList(pieces_data.PIECES_POSITION[key])

        glPopMatrix()

    glPopMatrix()

    previous = current

    glFlush();
    glutSwapBuffers()

##############################

def updateChessboard(current, previous):
    if (len(current) == 0 or len(previous) == 0):
        return

    result = np.zeros((8,8))
    for i in range(8):
        for j in range(8):
            result[i,j] = previous[i,j].value - current[i,j].value

    ## Aggiorno dizionario
    from_ = []
    to_ = []
    capture = []
    for i in range(8):
        for j in range(8):
            if result[i,j]!=0 and previous[i,j]!=Piece.EMPTY and current[i,j]!=Piece.EMPTY:
                capture = True
                to_= (i,j)
            elif result[i,j]<0 and (previous[i,j]!=Piece.EMPTY or current[i,j]!=Piece.EMPTY):
                from_= (i,j)
            elif result[i,j]!=0:
                to_= (i,j)

    if from_!=[] and to_!=[]:
        print(pieces_data.PIECES_POSITION)
        id = pieces_data.PIECES_POSITION[str(from_[0])+"-"+str(from_[1])]

        if capture == True:
            glDeleteLists(id, 1)

        del pieces_data.PIECES_POSITION[str(from_[0])+"-"+str(from_[1])]
        obj = pieces_data.PIECES_DICT[pieces_data.PIECES_CONV[previous[from_[0],from_[1]].name]]
        new_vertices = translateVertices(id, obj, *tuple(centers[to_[0],to_[1]]), z=2)
        overwriteList(id, obj, new_vertices)
        pieces_data.PIECES_POSITION[str(to_[0])+"-"+str(to_[1])] = id

        print(pieces_data.PIECES_POSITION)

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

def init_piece():
    global obj_s

    pieces = _chessboard.getPieces()
    print("DICT:",pieces_data.PIECES_DICT)

    ## Carico pezzi scacchi
    for i in range(8):
        for j in range(8):
            if pieces[i,j] != Piece.EMPTY:
                id = glGenLists(1)
                pieces_data.PIECES_POSITION[str(i)+"-"+str(j)] = id
                obj = pieces_data.PIECES_DICT[pieces_data.PIECES_CONV[pieces[i,j].name]]
                print("INDEX:",i,j)
                new_vertices = translateVertices(id, obj, *tuple(centers[i,j]), z=2)
                overwriteList(id, obj, new_vertices)

    ## Carico scacchiera
    pieces_data.id_chessboardList = glGenLists(1)
    obj = pieces_data.PIECES_DICT["Scacchiera"]
    overwriteList(pieces_data.id_chessboardList, obj, obj.vertices)

    ## Carico faccia del cubo per la selezione
    pieces_data.id_selectionSprite = glGenLists(1)
    obj_s = OBJ("resources/chess_models_reduced/Selection/selector.obj")
    new_vertices = translateVertices(pieces_data.id_selectionSprite, obj_s, *tuple(centers[0,0]), z=13)
    overwriteList(pieces_data.id_selectionSprite, obj_s, new_vertices)

    current = pieces

def init_gl():
    global chess_piece, texture_background, chess_piece2

    #glClearColor(0.7, 0.7, 0.7, 0.7)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    texture_background = glGenTextures(1)

###############################
# APPLICATION
def init_application():
    init_param()
    init_piece()
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
