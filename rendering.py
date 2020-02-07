import numpy as np
import cv2

def render (img, obj, projection_matrix):
    vertices = obj.vertices
    scale_matrix = np.eye(3) * 8
    for face in obj.mesh_list[0].faces:
        points = np.array([vertices[vertex - 1] for vertex in face])
        np_3d_points = np.asarray(points).astype(np.float32)
        np_3d_points = np.dot(np_3d_points, scale_matrix)
        _2d_points = cv2.perspectiveTransform(points.reshape(-1, 1, 3), projection_matrix)
        _2d_points = np.asarray(_2d_points).astype(np.int32)
        cv2.fillConvexPoly(img, _2d_points, (255,0,0))

    return img
