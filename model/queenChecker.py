from chessboard import *
from model_utils import *
from checker import *
import math

class QueenChecker(Checker):

    def checkMove(self, fromCell, toCell):
        print("### QUEEN CHECKER ###")

        chessboard = Chessboard.getInstance()

        fromCell_matrix = from_chessboard_to_matrix(fromCell)
        toCell_matrix = from_chessboard_to_matrix(toCell)

        ## Movimento sulla stessa riga
        if fromCell[1] == toCell[1]:
            print("Movimento sulla riga")

            max_row = max(fromCell_matrix[0],toCell_matrix[0])
            min_row = min(fromCell_matrix[0],toCell_matrix[0])

            for i in range(min_row+1,max_row):
                if chessboard.from_index_to_piece((i,fromCell_matrix[1])) != Piece.EMPTY.name:
                    raise Exception("[WrongMovementException]: Non si può scavalcare un pezzo")

            return True

        ## Movimento sulla stessa colonna
        if fromCell[0] == toCell[0]:
            print("Movimento sulla colonna")

            max_col = max(fromCell_matrix[1],toCell_matrix[1])
            min_col = min(fromCell_matrix[1],toCell_matrix[1])

            for i in range(min_col+1,max_col):
                print("check",(fromCell_matrix[0],i))
                if chessboard.from_index_to_piece((fromCell_matrix[0],i)) != Piece.EMPTY.name:
                    raise Exception("[WrongMovementException]: Non si può scavalcare un pezzo")

            return True

        ## Movimento in diagonale
        if abs(fromCell_matrix[0] - toCell_matrix[0]) == abs(fromCell_matrix[1] - toCell_matrix[1]):
            print("Movimento in diagonale")
            dir_x = ( toCell_matrix[0] - fromCell_matrix[0] ) / abs( toCell_matrix[0] - fromCell_matrix[0] )
            dir_y = ( toCell_matrix[1] - fromCell_matrix[1] ) / abs( toCell_matrix[1] - fromCell_matrix[1] )
            dir_x = int(dir_x)
            dir_y = int(dir_y)
            print("DIR:",dir_x,dir_y)

            steps = abs(fromCell_matrix[0] - toCell_matrix[0])
            for i in range(1,steps):
                print("check",(fromCell_matrix[0]+(i*dir_x),fromCell_matrix[1]+(i*dir_y)))
                if chessboard.from_index_to_piece((fromCell_matrix[0]+(i*dir_x),fromCell_matrix[1]+(i*dir_y))) != Piece.EMPTY.name:
                    raise Exception("[WrongMovementException]: Non si può scavalcare un pezzo")

            return True

        raise Exception("[RuleException]: Mossa errata!")
