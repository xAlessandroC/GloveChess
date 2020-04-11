from OpenGL.GL import *
import pieces_data as pieces_data
import numpy as np
import copy

def translate(vertices, x = 0, y = 0, z = 0):

    np_vertices = np.asarray(vertices).astype(np.float32)
    mean = np.mean(np_vertices,axis=0)
    # print("MEAN:", mean)
    # print("MOVE:",(x-mean[0]),(y-mean[1]))

    res = []
    for vertex in np_vertices:
        old_first = vertex[0]
        old_second = vertex[1]
        old_third = vertex[2]

        ##TRANSLATION
        new_first = old_first + x - mean[0]
        new_second = old_second + y - mean[1]
        new_third = old_third + z

        res.append([new_first,new_second,new_third])

    res = np.array(res).astype(np.float32)
    return res


def translateVertices(id_list, obj, x=0, y=0, z=0):
    print("TRANSLATION: ",x,y,z)

    new_vertices = translate(obj.vertices, x, y, z)

    return new_vertices

def overwriteList(id_list, obj, new_vertices):

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

def nearestCenter(centers, x, y, z):
    print("point:",(x,y))
    for i in range(centers.shape[0]):
        for j in range(centers.shape[1]):
            center = centers[i,j]
            point = np.array([x,y])

            distance = np.linalg.norm(center-point)
            print("distance from ",center,"=",distance)

            if distance < 2.5:
                return (i,j)


    return (-1,-1)
