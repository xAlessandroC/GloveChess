import sys
sys.path.append('../model/')

from chessboard import *
from executer import *

_chessboard = Chessboard.getInstance()
player = "WHITE"

def startPlayer(type):
    while _chessboard.isEnded() != True :
        currentTurn = Player(_chessboard.get_turn()[1]).name

        #SCEGLIE MOSSA
        if currentTurn == type:
            from_ = input("Please enter from value:\n")
            to_ = input("Please enter to value:\n")

            try:
                checkAndExecuteMove(from_, to_)
            except:
                pass
        # else:
        #     #MI SOSPENDO


    print("Il vincitore è:", _chessboard.getWinner())

if __name__ == "__main__":
    startPlayer()
