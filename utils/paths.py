test_path = "resources/marker/image_1.jpg"
video_path = "resources/marker/videooh_2.mp4"
model_path = "resources/marker/model.png"
obj_path = "resources/chess_models/Alfiere_Bianco/12929_WoodenChessBishopSideA_v1_l3.obj"
# obj_path = "resources/chess_models/Scacchiera/10586_Chess_Board_v2_Iterations-2.obj"
# obj_path = "resources/chess_models2/chess-horse-obj/chess-horse.obj"
# texture_path = "resources/chess_models/Alfiere_Bianco/12929_WoodenChessBishopSideA_diffuse.jpg"
texture_path = "resources/chess_models/Alfiere_Bianco/download.png"


# obj_path = "resources/chess_models/Random/Sting.obj"

###################################################


# import pywavefront
# import cv2
# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *
# import numpy as np
# import sys
#
# from objLoader import *
#
# global true_faces
# global texture_jpg, texture_id
#
# def init():
#     global texture_id
#
#     glClearColor(255.0, 0.0, 0.0, 1.0)
#
#     glutDisplayFunc(display)
#     glutIdleFunc(display)
#
#     img_data = np.frombuffer(texture_jpg.tostring(), np.uint8)
#
#     glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
#
#     glEnable(GL_TEXTURE_2D)
#     texture_id = glGenTextures(1)
#     glBindTexture( GL_TEXTURE_2D, texture_id )
#     glTexImage2D( GL_TEXTURE_2D, 0, 3, 1024, 1024, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data )
#
#     # glutPostRedisplay()
#
# def display():
#     global true_faces, texture_jpg, texture_id
#
#     glClearColor(0.0, 0.0, 0.0, 1.0)
#     glBindTexture(GL_TEXTURE_2D, texture_id)
#     glBegin( GL_QUADS )
#     for face in true_faces:
#         vertex = face[0]
#         texture = face[1]
#         for i in range(4):
#             # print(*texture[i])
#             glTexCoord2f(*texture[i])
#             glVertex3f(*vertex[i])
#     glEnd( )
#
#     glutSwapBuffers()
#     # print("finito")
#
# width = 800
# height = 600
# glutInit(sys.argv)
# glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
# glutInitWindowSize(width, height)
# glutInitWindowPosition(100, 100)
# glutCreateWindow("OpenGL + OpenCV")
#
# obj = OBJ(obj_path)
# texture_jpg = cv2.imread("resources/chess_models/Alfiere_Bianco/12929_WoodenChessBishopSideA_diffuse.jpg")
#
# true_faces = []
#
# vertices = obj.vertices
# texcoords = obj.texcoords
# for face in obj.faces:
#     true_vertices = np.array([vertices[vertex - 1] for vertex in face[0]]).astype(np.float32)
#     true_texcoords = np.array([texcoords[tx - 1] for tx in face[2]]).astype(np.float32)
#
#     true_faces.append((true_vertices,true_texcoords))
#
#
# init()
# glutMainLoop()
