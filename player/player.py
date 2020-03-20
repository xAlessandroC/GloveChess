import sys

from chessboard import *
from executer import *
from threading import Thread
from model_utils import *
import ARChess_application as main

_chessboard = Chessboard.getInstance()

class Player(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        while _chessboard.isEnded() != True :
            currentTurn = Turn(_chessboard.get_turn()[1]).name
            print("turno di ", currentTurn)
            print("Giocatore",self.name,": nuovo ciclo")

            #SCEGLIE MOSSA
            main.condition.acquire()
            currentTurn = Turn(_chessboard.get_turn()[1]).name
            if _chessboard.isEnded() == True:
                main.condition.release()

            elif currentTurn == self.name:
                # print("Giocatore",type,": lock acquisito")

                from_ = input("Giocatore "+self.name+" Please enter from value:\n")
                to_ = input("Giocatore "+self.name+" Please enter to value:\n")

                try:
                    checkAndExecuteMove(from_, to_)
                except:
                    pass

                main.condition.notifyAll()
                main.condition.release()

            else:
                print("Giocatore",self.name,": mi sospendo")
                main.condition.wait()

        print("Il vincitore è:", _chessboard.getWinner())
