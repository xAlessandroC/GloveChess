"""
    Implements the knight rules and generates all possible moves from a starting position.
"""

import math

from chessboard_model import Chessboard
from chess_enum import *
from model_utils import *
from generator import *

class KnightGenerator(Generator):

    def generateMoves(self, fromCell):

        moves = []
        chessboard = Chessboard.getInstance()
        pieces = chessboard.getPieces()
        currentTurn = Turn(chessboard.get_turn()[1]).name[0]

        fromCell_matrix = from_chessboard_to_matrix(fromCell)

        possibleMoves = []
        possibleMoves.append( (fromCell_matrix[0] + 2, fromCell_matrix[1] + 1) ) # L up-dx
        possibleMoves.append( (fromCell_matrix[0] + 2, fromCell_matrix[1] - 1) ) # L up-sx
        possibleMoves.append( (fromCell_matrix[0] - 2, fromCell_matrix[1] + 1) ) # L down-dx
        possibleMoves.append( (fromCell_matrix[0] - 2, fromCell_matrix[1] - 1) ) # L down-sx
        possibleMoves.append( (fromCell_matrix[0] + 1, fromCell_matrix[1] + 2) ) # L dx-up
        possibleMoves.append( (fromCell_matrix[0] - 1, fromCell_matrix[1] + 2) ) # L dx-down
        possibleMoves.append( (fromCell_matrix[0] + 1, fromCell_matrix[1] - 2) ) # L sx-up
        possibleMoves.append( (fromCell_matrix[0] - 1, fromCell_matrix[1] - 2) ) # L sx-down

        for to_cell in possibleMoves:
            if to_cell[0]>= 0 and to_cell[0]<8 and to_cell[1]>= 0 and to_cell[1]<8 and (pieces[to_cell].name.startswith(currentTurn) == False or pieces[to_cell] == Piece.EMPTY):
                moves.append(to_cell)

        return moves
