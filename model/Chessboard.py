import numpy as np
from model_utils import *
from piece import Piece

class Chessboard:
    __instance = None

    __centers = np.ndarray((8, 8))
    __pieces = np.ndarray((8, 8), dtype = int)
    __num_turns = 0
    __ended = False
    __winner = None

    @staticmethod
    def getInstance():
        if Chessboard.__instance == None:
            pieces = getInitialConfiguration()
            centers = np.zeros((8, 8))

            Chessboard(centers, pieces)

        return Chessboard.__instance

    def __init__(self, centers, pieces):
        if Chessboard.__instance != None:
            raise Exception("Chessboard is a singleton!")
        else:
            Chessboard.__instance = self
            self.__centers = centers
            self.__pieces = pieces
            self.__ended = False
            self.__winner = None


#   def __str__(self):
#       return "Mimino" + str(self.__centers.shape) + str(self.__pieces.shape)


    def increment_turn(self):
        self.__num_turns += 1

    def get_turn(self):
        if self.__num_turns % 2 == 0:
            return self.__num_turns, Player.WHITE.value
        else:
            return self.__num_turns, Player.BLACK.value

    def from_index_to_piece(self, index):
        if isinstance(index, str):
            index = from_chessboard_to_matrix(index)

        row_index = index[0]
        col_index = index[1]

        # print(self.__pieces)

        return Piece(self.__pieces[row_index, col_index]).name

    def update(self, fromCell, toCell):
        fromCell_matrix = from_chessboard_to_matrix(fromCell)
        toCell_matrix = from_chessboard_to_matrix(toCell)

        self.__pieces[toCell_matrix[0], toCell_matrix[1]] = self.__pieces[fromCell_matrix[0], fromCell_matrix[1]]
        self.__pieces[fromCell_matrix[0], fromCell_matrix[1]] = Piece.EMPTY

    def getPieces(self):
        return np.copy(self.__pieces)

    def isEnded(self):
        return self.__ended

    def setVictory(self, winner):
        self.__ended = True
        self.__winner = winner
        self.__num_turns = 0
        self.__pieces = getInitialConfiguration()

    def getWinner(self):
        return self.__winner
