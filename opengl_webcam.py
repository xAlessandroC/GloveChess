import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys

from calibration import *
from feature_detection import *
from rendering import *
from video import *
from paths import *
from objLoader import *

#window dimensions
width = 800
height = 600
nRange = 1.0

global capture
global camera_matrix
global obj
capture = None

def init():
  #glclearcolor (r, g, b, alpha)
  glClearColor(0.0, 0.0, 0.0, 1.0)

  glutDisplayFunc(display)
  glutReshapeFunc(reshape)
  glutKeyboardFunc(keyboard)
  glutIdleFunc(idle)

def renderObj():
    global obj

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, obj.model.itemsize * len(obj.model), obj.model, GL_STATIC_DRAW)

def idle():
  #capture next frame

  global capture
  ret, frame = capture.read()

  if not ret or frame is None:
      # Release the Video if ret is false
      capture.release()
      print("Released Video Resource")

  image_size = frame.shape

  ##Render
  test_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  img, projection_m = detect(test_image,camera_matrix,0)
  rendered_img = frame
  if projection_m.shape[0] != 0:
      rendered_img = render(frame, obj, projection_m, model_image)

  rendered_img = cv2.flip(rendered_img, -1)
  rendered_img = cv2.cvtColor(rendered_img, cv2.COLOR_BGR2RGB)
  #you must convert the image to array for glTexImage2D to work
  #maybe there is a faster way that I don't know about yet...
  img_data = np.frombuffer(rendered_img.tostring(), np.uint8

  # Create Texture
  global text
  # glBindTexture(GL_TEXTURE_2D, text);
  glTexImage2D(GL_TEXTURE_2D,
    0,
    GL_RGB,
    image_size[1],
    image_size[0],
    0,
    GL_RGB,
    GL_UNSIGNED_BYTE,
    img_data)

  # glBindTexture(GL_TEXTURE_2D, text);
  glutPostRedisplay()

def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glEnable(GL_TEXTURE_2D)
  # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
  # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
  # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
  #this one is necessary with texture2d for some reason
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

  # glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE );
  # glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE );

  # Set Projection Matrix
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluOrtho2D(0, width, 0, height)

  # Switch to Model View Matrix
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

  # Draw textured Quads
  glBegin(GL_QUADS)
  glTexCoord2f(0.0, 0.0)
  glVertex2f(0.0, 0.0)
  glTexCoord2f(1.0, 0.0)
  glVertex2f(width, 0.0)
  glTexCoord2f(1.0, 1.0)
  glVertex2f(width, height)
  glTexCoord2f(0.0, 1.0)
  glVertex2f(0.0, height)
  glEnd()

  glFlush()

  renderObj()
  glutSwapBuffers()

def reshape(w, h):
  if h == 0:
    h = 1

  glViewport(0, 0, w, h)
  glMatrixMode(GL_PROJECTION)

  glLoadIdentity()
  # allows for reshaping the window without distoring shape

  if w <= h:
    glOrtho(-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
  else:
    glOrtho(-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

def keyboard(key, x, y):
  global anim
  if key == chr(27):
    sys.exit()

def main():
  global capture
  global text
  global camera_matrix
  global obj
  #start openCV omCAM
  camera_matrix, dist_coefs, rvecs, tvecs = calibrate()
  obj = OBJ(obj_path)
  capture = cv2.VideoCapture(0)
  print("capture")
  capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutInitWindowSize(width, height)
  glutInitWindowPosition(100, 100)
  glutCreateWindow("OpenGL + OpenCV")

  # glEnable(GL_TEXTURE_2D);
  # text = glGenTextures(1)

  init()
  glutMainLoop()

main()
