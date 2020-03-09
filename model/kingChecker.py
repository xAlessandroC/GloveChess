from chessboard import Chessboard
from model_utils import *
from checker import *
import math

class KingChecker(Checker):

    def checkMove(self, fromCell, toCell):
        print("### KING CHECKER ###")
        limit = 1
        chessboard = Chessboard.getInstance()

        fromCell_matrix = from_chessboard_to_matrix(fromCell)
        toCell_matrix = from_chessboard_to_matrix(toCell)

        ## Movimento stessa riga
        if fromCell[1] == toCell[1]:
            print("Movimento sulla riga")

            steps = abs(toCell_matrix[0] - fromCell_matrix[0])
            print(steps)
            if steps != limit:
                raise Exception("[WrongMovementException]: Movimento troppo lungo!")

            return True

        ## Movimento stessa colonna
        if fromCell[0] == toCell[0]:
            print("Movimento sulla colonna")

            steps = abs(toCell_matrix[1] - fromCell_matrix[1])

            if steps != limit:
                raise Exception("[WrongMovementException]: Movimento troppo lungo!")

            return True

        ## Movimento in diagonale
        if abs(fromCell_matrix[0] - toCell_matrix[0]) == abs(fromCell_matrix[1] - toCell_matrix[1]):
            print("Movimento in diagonale")
            steps = abs(toCell_matrix[1] - fromCell_matrix[1])

            if steps != 1:
                raise Exception("[RuleException]: Movimento troppo lungo!")

            return True
        raise Exception("[RuleException]: Mossa errata!")
