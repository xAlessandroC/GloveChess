"""
    This module implements the interaction between human player and OpenGL main thread w.r.t. the selector mesh
"""

import settings as config
import glut_application as glta
import pieces_init as pieces_data
import register_functions as main

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from executer import *
from model_utils import *
from opengl_utils import *

from_ = ""
to_ = ""


def updateSelector():
    try:
        # Check for human player hand movement
        coords = config.queue_A.get(False)
        getCell(*coords)
    except:
        pass


def getCell(pos_x, pos_y):
    global from_, to_

    obj_s = glta.obj_s

    # Conversion between OpenCV coordinate system and OpenGL one
    tw = config.width_GL / config.width_CV
    th = config.height_GL / config.height_CV

    x = int(pos_x * tw)
    y = int(pos_y * th)

    projMatrix_r = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport_r = glGetIntegerv(GL_VIEWPORT)

    z_value = glReadPixels( x, config.height_GL-y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    world_coord = gluUnProject(x, config.height_GL-y, z_value, glta.current_mvm, projMatrix_r, viewport_r)
    world_coord = (world_coord[0], -world_coord[1], -world_coord[2])
    center_idx = nearestCenter(glta.centers, *world_coord)

    res = None
    if center_idx[0]>=0 and center_idx[1]>=0:
        new_vertices = translateVertices(obj_s, *tuple(glta.centers[center_idx[0], center_idx[1]]), z=13)
        overwriteList(pieces_data.id_selectionSprite, obj_s, new_vertices)
        res = center_idx

    # Return the selected cell
    config.queue_B.put(res)
    return
