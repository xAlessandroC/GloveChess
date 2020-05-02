"""
    This class define the human player
"""

import numpy as np
import settings as config
import glut_application as glta

from player import *
from finger_logic import *
from finger_extraction import *


class HumanPlayer(Player):

    def __init__(self, role):
        self.count = 0
        self.name = role
        self.previous = np.zeros((config.height_CV,config.width_CV,3))

    def doMove(self):
        result = False
        while result == False:
            frame = config.queue_img.get()
            fingers, bounding_r = finger_detection(frame)

            result = extract_move(fingers, bounding_r)

            self.previous = frame

        print("[HUMAN PLAYER]: executed move")
        return
