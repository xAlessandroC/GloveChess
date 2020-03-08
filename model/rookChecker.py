from chessboard import Chessboard
from model_utils import *
from checker import *
import math

class RookChecker(Checker):

    def checkMove(self, fromCell, toCell):
        print("### ROOK CHECKER ###")

        chessboard = Chessboard.getInstance()

        fromCell_matrix = chessboard.from_chessboard_to_matrix(fromCell)
        toCell_matrix = chessboard.from_chessboard_to_matrix(toCell)

        ## Movimento stessa riga
        if fromCell[1] == toCell[1]:
            print("Movimento sulla riga")

            max_row = max(fromCell_matrix[0], toCell_matrix[0])
            min_row = min(fromCell_matrix[0], toCell_matrix[0])

            for i in range(min_row + 1, max_row):
                if chessboard.from_index_to_piece((i, fromCell_matrix[1])) != Piece.EMPTY.name:
                    raise Exception("[WrongMovementException]: Impossibile scavalcare il pezzo")

            return True

        ## Movimento stessa colonna
        if fromCell[0] == toCell[0]:
            print("Movimento sulla colonna")

            max_col = max(fromCell_matrix[1], toCell_matrix[1])
            min_col = min(fromCell_matrix[1], toCell_matrix[1])

            for i in range(min_col+1,max_col):
                print("check",(fromCell_matrix[0], i))
                if chessboard.from_index_to_piece((fromCell_matrix[0], i)) != Piece.EMPTY.name:
                    raise Exception("[WrongMovementException]: Impossibile scavalcare il pezzo")

            return True

        raise Exception("[RuleException]: Mossa errata!")