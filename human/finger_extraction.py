"""
    This module implements hand detection use finger_utils for fingertips extraction.
"""

import cv2
import numpy as np
import settings as config

from finger_utils import *

def finger_detection(frame):
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_threshold = cv2.inRange(frame_HSV, (config.low_th[0],config.low_th[1],config.low_th[2]), (config.high_th[0],config.high_th[1],config.high_th[2]))

    _, contours, hierarchy = cv2.findContours(frame_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    maxArea = -1
    idx = -1
    # Find the biggest contour (according to area)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > maxArea:
            maxArea = area
            idx = i

    if idx != -1:
        selected_cnt = contours[idx]
        contoured_frame = np.copy(frame)
        hull = cv2.convexHull(selected_cnt)

        fingers_t, bounding_r = findFingers(contoured_frame, selected_cnt, hull)

        cv2.imshow("Glove window",contoured_frame)
        return fingers_t, bounding_r
    else:
        return ([],[])
