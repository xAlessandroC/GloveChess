"""
    This module compute the centers of the chessboard's cells
"""

import numpy as np

from objLoader_simple import *

length_x = 4.5
length_y = 4.5


def findCenters():
    # quite static function

    centers = []
    start = [15.7,15.7]
    for i in range(8):
        for j in range(8):
            centers.append([15.7-i*length_x,15.7-j*length_y])

    centers = np.array(centers).astype(np.float32)

    return centers
