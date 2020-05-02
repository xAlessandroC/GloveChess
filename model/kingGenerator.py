"""
    Implements the king rules and generates all possible moves from a starting position.
"""

import math

from chessboard import Chessboard
from chess_enum import *
from model_utils import *
from generator import *

class KingGenerator(Generator):

    def generateMoves(self, fromCell):

        moves = []
        chessboard = Chessboard.getInstance()
        pieces = chessboard.getPieces()
        currentTurn = Turn(chessboard.get_turn()[1]).name[0]

        fromCell_matrix = from_chessboard_to_matrix(fromCell)

        possibleMoves = []
        possibleMoves.append( (fromCell_matrix[0] + 1, fromCell_matrix[1]) ) #  up
        possibleMoves.append( (fromCell_matrix[0] - 1, fromCell_matrix[1]) ) #  down
        possibleMoves.append( (fromCell_matrix[0], fromCell_matrix[1] + 1) ) #  dx
        possibleMoves.append( (fromCell_matrix[0], fromCell_matrix[1] - 1) ) #  sx
        possibleMoves.append( (fromCell_matrix[0] + 1, fromCell_matrix[1] + 1) ) #  dx-up
        possibleMoves.append( (fromCell_matrix[0] - 1, fromCell_matrix[1] - 1) ) #  sx-down
        possibleMoves.append( (fromCell_matrix[0] + 1, fromCell_matrix[1] - 1) ) #  dx-down
        possibleMoves.append( (fromCell_matrix[0] - 1, fromCell_matrix[1] + 1) ) #  sx-up

        for to_cell in possibleMoves:
            if to_cell[0]>= 0 and to_cell[0]<8 and to_cell[1]>= 0 and to_cell[1]<8 and (pieces[to_cell].name.startswith(currentTurn) == False or pieces[to_cell] == Piece.EMPTY):
                moves.append(to_cell)

        return moves
