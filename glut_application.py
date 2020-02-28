from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import cv2

from objloader_complete import *
from utils.paths import *
from utils.calibration import *
from ppm_formula import *

from PIL import Image

import ctypes

from aruco import *

###############################
# GLOBAL VARIABLES
width = 1280
height = 720
texture_background = None
chess_piece = None
webcam = cv2.VideoCapture(0)
camera_matrix, dist_coefs, rvecs, tvecs = calibrate()

znear = 0.1
zfar = 10000.0

###############################

############################### INIT OPENGL
def init_gl():
    global texture_background, chess_piece

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    # glDepthFunc(GL_LESS)
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.34, 1.78, znear, zfar)   #Cambiare all'occorrenza
    glViewport(0,0,width,height)

    # ppm = getOpenglProjectionMatrix(camera_matrix, znear, zfar, width, height)
    # # glMatrixMode(GL_PROJECTION)
    # # glPushMatrix()
    # glLoadMatrixf(ppm)

    glMatrixMode(GL_MODELVIEW)

    # assign shapes
    chess_piece = OBJ(obj_path, True)

    # assign texture
    glEnable(GL_TEXTURE_2D)
    texture_background = glGenTextures(1)

############################### WEBCAM HANDLER
def getNextFrame():
    global webcam

    ret, frame = webcam.read()

    if not ret or frame is None:
        webcam.release()
        print("Released webcam")
        return None

    return frame

############################### WINDOWS FUNCTION
def draw_background(image):
    global texture_background

    bg_image = cv2.flip(image, 0)
    bg_image = Image.fromarray(bg_image)
    ix = bg_image.size[0]
    iy = bg_image.size[1]
    bg_image = bg_image.tobytes("raw", "BGRX", 0, -1)

    # create background texture
    glBindTexture(GL_TEXTURE_2D, texture_background)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_image)

    # draw background
    glBindTexture(GL_TEXTURE_2D, texture_background)
    glPushMatrix()
    glTranslatef(0.0,0.0,-10.0)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 3.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 3.0)
    glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 3.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 3.0)
    glEnd( )

    glPopMatrix()

def draw_obj(rvec, tvec, center, p_k):

    ### OBTAINING PROJECTION MATRIX
    view_matrix = getCorrectPPM(rvec,tvec)
    # view_matrix = tryThis(p_k)

    ###############################
    lightfv = ctypes.c_float * 4
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    glEnable(GL_LIGHT0)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadMatrixd(view_matrix)
    glTranslatef(0.0, 0.0, -100.0)
    # glTranslatef(-center[0], center[1], 0.0)
    # glRotatef(-90, 1.0, 0.0, 0.0)
    glEnable(GL_LIGHTING)

    glCallList(chess_piece.gl_list)

    glColor3f(1.0, 1.0, 1.0)
    glPopMatrix()
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)


def display():
    global chess_piece, camera_matrix, dist_coefs

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    image = getNextFrame()

    rvec, tvec, frame, center, p_k = detect(image, camera_matrix, dist_coefs, chess_piece)

    draw_background(frame)

    if len(rvec) != 0 and len(tvec) != 0:
        draw_obj(rvec, tvec, center, p_k)

    glutSwapBuffers()


def reshape():
    if height == 0:
      height = 1

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    if width <= height:
      glOrtho(-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
    else:
      glOrtho(-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


############################### APPLICATION
def init_application():
    print("Initializing app")
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("AR Chess")

    glutDisplayFunc(display)
    glutIdleFunc(display)
    # glutReshapeFunc(reshape)

    init_gl()
    print("Inizialization completed")
    glutMainLoop()



init_application()
