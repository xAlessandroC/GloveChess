"""
    This module defines some utility functions
    *   getPossibleMoves: generates all possible moves starting from the current state and the type of player
    *   nextState: return the resulting state after a possible move
    *   heuristic: implement a very simple heuristic used by minmax
"""

from chess_enum import Piece
from model_utils import *
from action import *

def getPossibleMoves(node, role):

    state = node.getState()

    moves = []
    for i in range(8):
        for j in range(8):
            if state[i][j].name.startswith(role[0]):
                piece = state[i][j].name
                # Use the generators of model
                generatorName = piece[2:].lower() + "Generator"
                module = __import__(generatorName)
                class_ = getattr(module, generatorName[0].upper()+generatorName[1:])
                instance = class_()

                possibleMoves = instance.generateMoves(from_matrix_to_chessboard((i,j)))
                for move in possibleMoves:
                    action = Action(from_matrix_to_chessboard((i,j)),from_matrix_to_chessboard(move))
                    moves.append(action)

    return moves


def nextState(node, move):

    state = node.getState()

    print(move.getFrom(), move.getTo())
    fromCell_matrix = from_chessboard_to_matrix(move.getFrom())
    toCell_matrix = from_chessboard_to_matrix(move.getTo())

    state_copy = np.copy(state)
    state_copy[toCell_matrix[0], toCell_matrix[1]] = state_copy[fromCell_matrix[0], fromCell_matrix[1]]
    state_copy[fromCell_matrix[0], fromCell_matrix[1]] = Piece.EMPTY

    return state_copy

def getOtherRole(role):
    if role == "WHITE":
        return "BLACK"
    else:
        return "WHITE"


WEIGHTS = {
    "PAWN" : 1,
    "ROOK" : 5,
    "KNIGHT" : 3,
    "BISHOP" : 3,
    "KING" : 10,
    "QUEEN" : 9,
}

def heuristic(node, role):

    state = node.getState()

    num_W = 0
    num_B = 0

    num_controlled_cells = 0

    king_threatened = 0
    king_pos = (-1,-1)

    for i in range(8):
        for j in range(8):
            piece_name = state[i][j].name

            if piece_name[2:] == "KING" and  piece_name.startswith(role[0]):
                king_pos = (i,j)

            # Value of state
            if piece_name.startswith("W"):
                num_W = num_W + WEIGHTS[piece_name[2:]]
            if piece_name.startswith("B"):
                num_B = num_B + WEIGHTS[piece_name[2:]]

            # Space dominance
            if piece_name.startswith(role[0]):
                generatorName = piece_name[2:].lower() + "Generator"
                module = __import__(generatorName)
                class_ = getattr(module, generatorName[0].upper()+generatorName[1:])
                instance = class_()

                possibleMoves = instance.generateMoves(from_matrix_to_chessboard((i,j)))
                num_controlled_cells = len(possibleMoves)


    if king_pos == (-1,-1):
        king_threaten = 1
        print("king threatened")

    if role == "WHITE":
        return (num_W - num_B) #+ num_controlled_cells - (king_threatened*20)
    if role == "BLACK":
        return (num_B - num_W) #+ num_controlled_cells - (king_threatened*20)
