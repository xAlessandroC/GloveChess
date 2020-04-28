from model_utils import *
from action import *

def getPossibleMoves(node, role):

    state = node.getState()

    moves = []
    for i in range(len(8)):
        for j in range(len(8)):
            if state[i][j].name.startswith(role[0]):
                generatorName = piece[2:].lower() + "Generator"
                module = __import__(generatorName)
                class_ = getattr(module, generatorName[0].upper()+generatorName[1:])
                instance = class_()

                possibleMoves = instance.generateMoves(from_matrix_to_chessboard((i,j)))
                for move in possibleMoves:
                    action = Action(from_matrix_to_chessboard((i,j)),move)
                    moves.append(action)

    return moves


def nextState(node, move):

    state = node.getState()

    fromCell_matrix = from_chessboard_to_matrix(move.getFrom())
    toCell_matrix = from_chessboard_to_matrix(move.getTo())

    state_copy = np.copy(state)
    state_copy[toCell_matrix[0], toCell_matrix[1]] = state_copy[fromCell_matrix[0], fromCell_matrix[1]]
    state_copy[fromCell_matrix[0], fromCell_matrix[1]] = Piece.EMPTY

    return state_copy

def heuristic(node, role):

    state = node.getState()

    num_W = 0
    num_B = 0

    for i in range(len(8)):
        for j in range(len(8)):
            if state[i][j].name.startswith("W"):
                num_W = num_W + 1
            if state[i][j].name.startswith("B"):
                num_B = num_B + 1


    if role == "WHITE":
        return (num_W - num_B) * 10
    if role == "BLACK":
        return (num_B - num_W) * 10
