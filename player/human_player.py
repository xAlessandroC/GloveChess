import glut_application as glta
import register_functions as main
import numpy as np

from finger import *
from player import *
from finger_logic import *

class HumanPlayer(Player):

    def __init__(self, role):
        self.count = 0
        self.name = role
        self.previous = np.zeros((720,1280,3))

    def doMove(self):
        print("ciao HUMAN")
        result = False
        while result == False:
            frame = glta.queue_img.get()
            fingers, bounding_r = finger_detection(frame)

            result = extract_move(fingers, bounding_r)

            self.previous = frame

        print("[HUMAN PLAYER]: mossa fatta, adios")
        return
