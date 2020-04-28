from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import glut_application as glta
import pieces_data as pieces_data
import register_functions as main
from opengl_utils import *
from model_utils import *
from executer import *

from_ = ""
to_ = ""

def updateSelector():
    try:
        coords = glta.queue_A.get(False)
        print("[MAIN_THREAD: Ricevuto da A",coords,"]")
        getCell(*coords)
    except:
        pass

def getCell(x, y):
    global from_, to_
    obj_s = glta.obj_s

    projMatrix_r = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport_r = glGetIntegerv(GL_VIEWPORT)

    z_value = glReadPixels( x, 720-y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    world_coord = gluUnProject(x, 720-y, z_value, glta.current_mvm, projMatrix_r, viewport_r)
    world_coord = (world_coord[0], -world_coord[1], -world_coord[2])
    center_idx = nearestCenter(glta.centers, *world_coord)

    print("CENTER_IDX:", center_idx)
    res = None
    if center_idx[0]>=0 and center_idx[1]>=0:
        new_vertices = translateVertices(pieces_data.id_selectionSprite, obj_s, *tuple(glta.centers[center_idx[0], center_idx[1]]), z=13)
        overwriteList(pieces_data.id_selectionSprite, obj_s, new_vertices)
        res = center_idx

    print("[MAIN_THREAD: Mando su B",res,"]")
    glta.queue_B.put(res)
    return
