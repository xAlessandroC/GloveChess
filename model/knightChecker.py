from chessboard import Chessboard
from model_utils import *
from checker import *
import math

class KnightChecker(Checker):

    def checkMove(self, fromCell, toCell):
        print("### KNIGHT CHECKER ###")

        #chessboard = Chessboard.getInstance()

        fromCell_matrix = from_chessboard_to_matrix(fromCell)
        toCell_matrix = from_chessboard_to_matrix(toCell)

        rightMoves = []
        rightMoves.append( (fromCell_matrix[0] + 2, fromCell_matrix[1] + 1) ) # L superiore a destra
        rightMoves.append( (fromCell_matrix[0] + 2, fromCell_matrix[1] - 1) ) # L superiore a sinistra
        rightMoves.append( (fromCell_matrix[0] - 2, fromCell_matrix[1] + 1) ) # L inferiore a destra
        rightMoves.append( (fromCell_matrix[0] - 2, fromCell_matrix[1] - 1) ) # L inferiore a sinistra
        rightMoves.append( (fromCell_matrix[0] + 1, fromCell_matrix[1] + 2) ) # L a destra-su
        rightMoves.append( (fromCell_matrix[0] - 1, fromCell_matrix[1] + 2) ) # L a destra-giù
        rightMoves.append( (fromCell_matrix[0] + 1, fromCell_matrix[1] - 2) ) # L a sinistra-su
        rightMoves.append( (fromCell_matrix[0] - 1, fromCell_matrix[1] - 2) ) # L a sinistra-giù

        for cell in rightMoves:
            if toCell_matrix == cell:
                # da controllare se in toCell c'è un tuo pezzo?
                return True

        raise Exception("[RuleException]: Mossa errata!")
