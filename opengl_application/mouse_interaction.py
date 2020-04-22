from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import glut_application as glt_app
import pieces_data as pieces_data
from opengl_utils import *
from model_utils import *
from executer import *

from_ = ""
to_ = ""

def mouse(button, state, x, y):
    global from_, to_
    obj_s = glt_app.obj_s

    projMatrix_r = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport_r = glGetIntegerv(GL_VIEWPORT)

    if state == GLUT_DOWN:
        z_value = glReadPixels( x, 720-y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        world_coord = gluUnProject(x, 720-y, z_value, glt_app.current_mvm, projMatrix_r, viewport_r)
        world_coord = (world_coord[0], -world_coord[1], -world_coord[2])

        center_idx = nearestCenter(glt_app.centers, *world_coord)
        print("CENTER_IDX:", center_idx)
        if center_idx[0]>=0 and center_idx[1]>=0:
            new_vertices = translateVertices(pieces_data.id_selectionSprite, obj_s, *tuple(glt_app.centers[center_idx[0], center_idx[1]]), z=13)
            overwriteList(pieces_data.id_selectionSprite, obj_s, new_vertices)
            print("CHESSBOARD POSITION:", from_matrix_to_chessboard(center_idx))
            from_=from_matrix_to_chessboard(center_idx)

    if state == GLUT_UP:
        z_value = glReadPixels( x, 720-y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        world_coord = gluUnProject(x, 720-y, z_value, glt_app.current_mvm, projMatrix_r, viewport_r)
        world_coord = (world_coord[0], -world_coord[1], -world_coord[2])

        center_idx = nearestCenter(glt_app.centers, *world_coord)
        print("CENTER_IDX:", center_idx)
        if center_idx[0]>=0 and center_idx[1]>=0:
            print("CHESSBOARD POSITION:", from_matrix_to_chessboard(center_idx))
            if from_ != "":
                to_ = from_matrix_to_chessboard(center_idx)
                try:
                    checkAndExecuteMove(from_, to_)
                    new_vertices = translateVertices(pieces_data.id_selectionSprite, obj_s, *tuple(glt_app.centers[center_idx[0], center_idx[1]]), z=13)
                    overwriteList(pieces_data.id_selectionSprite, obj_s, new_vertices)
                except:
                    pass
                from_ = ""
                to_ = ""

        print("MVM:",glt_app.current_mvm)
        print("[VIEWPORT]: Button click at ",x,y)
        print("Z-VALUE:", z_value)
        print("3D COORD:", world_coord)
