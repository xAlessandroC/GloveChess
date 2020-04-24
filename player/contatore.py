import sys
import os
import signal
import register_functions as main
import glut_application as glta
import numpy as np

from chessboard import *
from executer import *
from model_utils import *
from threading import Thread
from finger import *

_chessboard = Chessboard.getInstance()

class Thread_A(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.count = 0
        self.previous = np.zeros((720,1280,3))

    def run(self):
        while True:
            frame = glta.webcam.getLastFrame()
            # print(frame != self.previous)
            if np.all(frame == self.previous) == False:
                self.count = self.count + 1
                finger_detection(frame)
                print("[HUMAN]: Frame", self.count)

            self.previous = frame

    def terminate(self):
        self.stop = True
        os.kill(os.getpid(), signal.SIGINT)
