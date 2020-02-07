import ctypes
import os
import sys

sys.path.append('..')

import pyglet
from pyglet.gl import *

from pywavefront import visualization
import pywavefront

print("ciao")
# Create absolute path from this module
dirname = "resources/chess_models/Alfiere_Bianco/"
fn = dirname + "12929_WoodenChessBishopSideA_diffuse.jpg"
file_abspath=dirname + "12929_WoodenChessBishopSideA_v1_l3.obj"

print(file_abspath)
rotation = 0
meshes = pywavefront.Wavefront(file_abspath)
window = pyglet.window.Window(resizable=True)
lightfv = ctypes.c_float * 4


@window.event
def on_resize(width, height):
    viewport_width, viewport_height = window.get_framebuffer_size()
    glViewport(0, 0, viewport_width, viewport_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., float(width)/height, 1., 100.)
    glMatrixMode(GL_MODELVIEW)
    return True


@window.event
def on_draw():
    window.clear()
    glLoadIdentity()


#    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
#    glEnable(GL_LIGHT0)

    glTranslated(0.0, 0.0, -50.0)
    glRotatef(0, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    glRotatef(0, 0.0, 0.0, 1.0)

    glEnable(GL_LIGHTING)

    visualization.draw(meshes)


def update(dt):
    global rotation
    rotation += 90.0 * dt

    if rotation > 720.0:
        rotation = 0.0


pyglet.clock.schedule(update)
pyglet.app.run()
