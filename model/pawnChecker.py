from chessboard import *
from model_utils import *
from checker import *
import math

class PawnChecker(Checker):

    __B_startPosition = ["a7","b7","c7","d7","e7","f7","g7","h7"]
    __W_startPosition = ["a2","b2","c2","d2","e2","f2","g2","h2"]

    def checkMove(self, fromCell, toCell):
        print("### PAWN CHECKER ###")

        chessboard = Chessboard.getInstance()

        currentTurn = Turn(chessboard.get_turn()[1]).name

        fromCell_matrix = from_chessboard_to_matrix(fromCell)
        toCell_matrix = from_chessboard_to_matrix(toCell)

        limit = 1
        direction = 0
        if currentTurn == "WHITE":
            direction = 1
            if fromCell in self.__W_startPosition:
                limit = 2

        if currentTurn == "BLACK":
            direction = -1
            if fromCell in self.__B_startPosition:
                limit = 2

        print("limit:", limit)

        steps = (toCell_matrix[1] - fromCell_matrix[1]) * direction
        if steps <= 0:
            raise Exception("[RuleException]: Movimento all'indietro!")

        #Movimento
        if fromCell[0] == toCell[0]:

            if steps > limit:
                raise Exception("[RuleException]: Movimento troppo lungo!")

            if chessboard.from_index_to_piece(toCell) != Piece.EMPTY.name:
                raise Exception("[RuleException]: Mangiata verticale!")

            if limit == 2 and chessboard.from_index_to_piece((fromCell_matrix[0],fromCell_matrix[1]+(1*direction))) != Piece.EMPTY.name:
                raise Exception("[WrongMovementException]: Non si può scavalcare un pezzo")

            return True

        #Mangiata
        if abs(fromCell_matrix[0] - toCell_matrix[0]) == abs(fromCell_matrix[1] - toCell_matrix[1]):
            steps = abs(toCell_matrix[1] - fromCell_matrix[1])

            if steps != 1:
                raise Exception("[RuleException]: Movimento troppo lungo!")

            if chessboard.from_index_to_piece(toCell) == Piece.EMPTY.name:
                raise Exception("[RuleException]: Movimento diagonale!")

            return True

        raise Exception("[RuleException]: Mossa errata!")
