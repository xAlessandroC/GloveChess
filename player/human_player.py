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
            frame = glta.webcam.getLastFrame()
            if np.all(frame == self.previous) == False:
                self.count = self.count + 1
                # print("[HUMAN PLAYER]: Elaboro frame n", self.count)
                fingers, bounding_r = finger_detection(frame)

                result = extract_move(fingers, bounding_r)

            else:
                # print("[HUMAN PLAYER]: wait...")
                main.lock_img.acquire()

            self.previous = frame

        print("[HUMAN PLAYER]: mossa fatta, adios")
        return
