from chessboard import Chessboard
from model_utils import *
from generator import *
import math

class RookGenerator(Generator):

    def generateMoves(self, fromCell):
        print("### ROOK GENERATOR ###")

        moves = []
        chessboard = Chessboard.getInstance()
        pieces = chessboard.getPieces()
        currentTurn = Turn(chessboard.get_turn()[1]).name[0]

        fromCell_matrix = from_chessboard_to_matrix(fromCell)

        climb_1 = False
        climb_2 = False
        climb_3 = False
        climb_4 = False
        for i in range(1,8):

            # fromCell[0] + i, fromCell[1]  dx
            if fromCell_matrix[0] + i < 8 and climb_1 == False:
                to_cell = (fromCell_matrix[0] + i, fromCell_matrix[1])

                if pieces[to_cell] == Piece.EMPTY:
                    moves.append(to_cell)

                elif pieces[to_cell].name.startswith(currentTurn) == False:
                    moves.append(to_cell)
                    climb_1 = True
                else:
                    climb_1 = True

            # fromCell[0], fromCell[1] + i  up
            if fromCell_matrix[1] + i < 8 and climb_2 == False:
                to_cell = (fromCell_matrix[0], fromCell_matrix[1] + i)

                if pieces[to_cell] == Piece.EMPTY:
                    moves.append(to_cell)

                elif pieces[to_cell].name.startswith(currentTurn) == False:
                    moves.append(to_cell)
                    climb_2 = True
                else:
                    climb_2 = True

            # fromCell[0] - i, fromCell[1]   sx
            if fromCell_matrix[0] - i >= 0 and climb_3 == False:
                to_cell = (fromCell_matrix[0] - i, fromCell_matrix[1])

                if pieces[to_cell] == Piece.EMPTY:
                    moves.append(to_cell)

                elif pieces[to_cell].name.startswith(currentTurn) == False:
                    moves.append(to_cell)
                    climb_3 = True
                else:
                    climb_3 = True

            # fromCell[0], fromCell[1] - i   down
            if fromCell_matrix[1] - i >= 0 and climb_4 == False:
                to_cell = (fromCell_matrix[0], fromCell_matrix[1] - i)

                if pieces[to_cell] == Piece.EMPTY:
                    moves.append(to_cell)

                elif pieces[to_cell].name.startswith(currentTurn) == False:
                    moves.append(to_cell)
                    climb_4 = True
                else:
                    climb_4 = True

        return moves
