"""
    This module implements the movement's logic for selecting and moving the pieces
"""

import settings as config
import glut_application as glta

from model_utils import *
from executer import *

from_f = None
to_f = None
last_selected_f = None
logic_state = "FROM"

def extract_move(fingers, bounding_r):
    global logic_state, from_f, to_f, last_selected_f

    result = False

    # We assume that the returned points consist in fingertips only
    fingers_number = len(fingers)

    # 5 fingers -> movement of selector
    if fingers_number >= 5:

        # Pick the middle finger
        selected_finger = fingers[getMiddleFinger(fingers, bounding_r)]

        # Interaction with opengl module
        config.queue_A.put(selected_finger)

        # Opengl module returns selected cell
        t = config.queue_B.get()
        if t != None:
            last_selected_f = t

    # 2 fingers -> piece selection
    elif fingers_number == 2:

        # Finite state machine to capture both from and to cell
        if logic_state == "FROM" and last_selected_f != None:
            print("[HUMAN PLAYER]: selected from ", last_selected_f)
            from_f = last_selected_f
            logic_state = "TO"

        elif logic_state == "TO" and last_selected_f != from_f:
            print("[HUMAN PLAYER]: selected to ", last_selected_f)
            to_f = last_selected_f
            logic_state = "FROM"

        # Excute movement
        if from_f != None and to_f != None and last_selected_f != None:

            from_m = from_matrix_to_chessboard(from_f)
            to_m = from_matrix_to_chessboard(to_f)
            print("[HUMAN PLAYER]: faccio mossa ", from_f, to_f)
            try:
                checkAndExecuteMove(from_m, to_m)
                result = True
            except Exception as e:
                print(e)

            from_f = None
            to_f = None


    return result

def getMiddleFinger(fingers, bounding_r):
    # We want to be invariant to different position of hand

    # Extract the right hand orientation
    k = -1
    if bounding_r[2]>= bounding_r[3]:
        k = 0
    else:
        k = 1

    # Compute center of the given bounding rect
    center = (int(bounding_r[0]+bounding_r[2]/2), int(bounding_r[1]+bounding_r[3]/2))
    max = 0
    min = 0

    # Extract hand direction comparing the given finger with the center
    for i in range(len(fingers)):
        if fingers[i][k] > center[k]:
            max = max + 1
        else:
            min = min + 1

    temp = None

    # Extract the right coordinate of middle finger (maxima extrema of fingertips)
    if max > min : temp = np.array(fingers)[:,k].max()
    else:  temp = np.array(fingers)[:,k].min()

    # Retrieve the finger which have the temp coordinate
    for i in range(len(fingers)):
        if fingers[i][k] == temp:
            return i


    return -1
