import sys
import os
import signal
import register_functions as main

from chessboard import *
from executer import *
from model_utils import *
from threading import Thread

_chessboard = Chessboard.getInstance()

class Thread_P(Thread):
    def __init__(self, typeOfPlayer):
        Thread.__init__(self)
        self.typeOfPlayer = typeOfPlayer
        self.stop = False

    def run(self):
        while _chessboard.isEnded() != True and self.stop == False :
            currentTurn = Turn(_chessboard.get_turn()[1]).name
            print("turno di ", currentTurn)
            print("Giocatore",self.typeOfPlayer.name,": nuovo ciclo")

            #SCEGLIE MOSSA
            event = _chessboard.getPlayerEvent(self.typeOfPlayer.name)
            event.wait()
            event.clear()
            print("Giocatore",self.typeOfPlayer.name,": mio turno")

            self.typeOfPlayer.doMove()

        print("Il vincitore è:", _chessboard.getWinner())

    def terminate(self):
        self.stop = True
        os.kill(os.getpid(), signal.SIGINT)
