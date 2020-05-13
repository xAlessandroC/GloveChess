"""
    Implements the pawn rules and generates all possible moves from a starting position
"""

import math

from chessboard_model import *
from chess_enum import *
from model_utils import *
from generator import *

class PawnGenerator(Generator):

    __B_startPosition = ["a7","b7","c7","d7","e7","f7","g7","h7"]
    __W_startPosition = ["a2","b2","c2","d2","e2","f2","g2","h2"]

    def generateMoves(self, fromCell):

        moves = []
        chessboard = Chessboard.getInstance()
        pieces = chessboard.getPieces()
        currentTurn = Turn(chessboard.get_turn()[1]).name[0]

        fromCell_matrix = from_chessboard_to_matrix(fromCell)

        limit = 1
        direction = 0
        if currentTurn == "W":
            direction = 1
            if fromCell in self.__W_startPosition:
                limit = 2

        if currentTurn == "B":
            direction = -1
            if fromCell in self.__B_startPosition:
                limit = 2

        climb = False
        for i in range(1, limit+1):
            to_cell = (fromCell_matrix[0], fromCell_matrix[1] + (i*direction))
            if to_cell[0]>= 0 and to_cell[0]<8 and to_cell[1]>= 0 and to_cell[1]<8 and climb==False:
                if pieces[to_cell] == Piece.EMPTY:
                    moves.append(to_cell)
                if pieces[to_cell] != Piece.EMPTY:
                    climb = True

        to_cell = (fromCell_matrix[0] + 1, fromCell_matrix[1] + direction)
        if to_cell[0]>= 0 and to_cell[0]<8 and to_cell[1]>= 0 and to_cell[1]<8 and (pieces[to_cell] != Piece.EMPTY and pieces[to_cell].name.startswith(currentTurn) == False):
            moves.append(to_cell)

        to_cell = (fromCell_matrix[0] - 1, fromCell_matrix[1] + direction)
        if to_cell[0]>= 0 and to_cell[0]<8 and to_cell[1]>= 0 and to_cell[1]<8 and (pieces[to_cell] != Piece.EMPTY and pieces[to_cell].name.startswith(currentTurn) == False):
            moves.append(to_cell)

        return moves
