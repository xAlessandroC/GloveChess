from movepiece import *
from OpenGL.GL import *
import pieces_data as pieces_data
import copy


def translateVertices(id_list, name, x=0, y=0):
    print("TRANSLATION: ",x,y)

    obj = pieces_data.PIECES_DICT[pieces_data.PIECES_CONV[name]]
    new_vertices = translate(obj.vertices, x, y)

    glNewList(id_list, GL_COMPILE)
    glEnable(GL_TEXTURE_2D)
    glFrontFace(GL_CCW)
    for face in obj.faces:
        vertices, normals, texture_coords, material = face

        mtl = obj.mtl[material]
        if 'texture_Kd' in mtl:
            # use diffuse texmap
            glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
        else:
            # just use diffuse colour
            glColor(*mtl['Kd'])

        glBegin(GL_POLYGON)
        for i in range(len(vertices)):
            if normals[i] > 0:
                glNormal3fv(obj.normals[normals[i] - 1])
            if texture_coords[i] > 0:
                glTexCoord2fv(obj.texcoords[texture_coords[i] - 1])
            glVertex3fv(new_vertices[vertices[i] - 1])
        glEnd()
    glDisable(GL_TEXTURE_2D)
    glEndList()

    return obj
