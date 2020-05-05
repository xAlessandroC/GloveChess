"""
    This class define the IA player
"""

from player import *
from chessboard_model import *
from executer import *
from minmax import *

class IAPlayer(Player):

    def __init__(self, role):
        self.name = role

    def doMove(self):
        _chessboard = Chessboard.getInstance().getPieces()
        move = minmax(_chessboard, 4, self.name)

        print("[IA PLAYER]: chosen move ", move.getFrom(), move.getTo())
        if move != None:
            checkAndExecuteMove(move.getFrom(), move.getTo())
