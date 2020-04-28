from player import *
from chessboard import *
from executer import *
from model_utils import *
from minmax import *

class IAPlayer(Player):

    def __init__(self, role):
        self.name = role

    def doMove(self):
        print("ciao IA")
        
        # Prendere lo stato attuale
        _chessboard = Chessboard.getInstance().getPieces()

        # Avvii min-max con lo stato attuale
        move = minmax(_chessboard, 3, self.name)

        # Effettua la mossa
        print(move)
