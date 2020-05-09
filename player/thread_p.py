"""
    Define the player thread model.
"""

import os
import signal

from threading import Thread
from chessboard_model import *
from executer import *
from chess_enum import *

_chessboard = Chessboard.getInstance()

class Thread_P(Thread):
    def __init__(self, typeOfPlayer):
        Thread.__init__(self)
        self.typeOfPlayer = typeOfPlayer
        self.stop = False

    def run(self):
        while _chessboard.isEnded() != True and self.stop == False :
            currentTurn = Turn(_chessboard.get_turn()[1]).name
            print("Current turn:", currentTurn)

            event = _chessboard.getPlayerEvent(self.typeOfPlayer.name)
            event.wait()
            event.clear()

            self.typeOfPlayer.doMove()

        print("The winner is ", _chessboard.getWinner())

    def terminate(self):
        self.stop = True
        os.kill(os.getpid(), signal.SIGINT)
