from utils.objloader_simple import *
import utils.config as config
import numpy as np

length_x = 4.5
length_y = 4.5

def findCenters():

    scacchiera = OBJSimple(config.obj_path)

    vertices = np.array(scacchiera.vertices).astype(np.float32)

    max_coords = vertices.max(axis=0)
    min_coords = vertices.min(axis=0)

    v1 = np.array([max_coords[0], max_coords[1], max_coords[2]])
    v2 = np.array([min_coords[0], max_coords[1], max_coords[2]])
    v3 = np.array([max_coords[0], min_coords[1], max_coords[2]])
    v4 = np.array([min_coords[0], min_coords[1], max_coords[2]])

    # #VERTICI DELLA SCACCHIERA 3D
    # print("V1:",v1) #alto a destra
    # print("V2:",v2) #alto a sinistra
    # print("V3:",v3) #basso a destra
    # print("V4:",v4) #basso a sinistra

    centers = []
    start = [15.7,15.7]
    for i in range(8):
        for j in range(8):
            centers.append([15.7-i*length_x,15.7-j*length_y])

    centers = np.array(centers).astype(np.float32)

    return centers
