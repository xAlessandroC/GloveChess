"""
    Implements several checks and updates chessboard with the specified move.
"""

from chessboard_model import *
from model_utils import *


def checkAndExecuteMove(fromCell, toCell):

    chessboard = Chessboard.getInstance()

    currentTurn = Turn(chessboard.get_turn()[1]).name
    selectedPiece = chessboard.from_index_to_piece(fromCell)
    destPiece = chessboard.from_index_to_piece(toCell)

    print("### EXECUTER ###\nCurrent Turn:",currentTurn,"\nSelectedPiece:", selectedPiece)
    print("Chessboard from:", fromCell,"\nMatrix from:",from_chessboard_to_matrix(fromCell))
    print("Chessboard to:", toCell,"\nMatrix to:",from_chessboard_to_matrix(toCell))

    if selectedPiece[0] != currentTurn[0] :
        raise Exception("[WrongTurnException]: You must move your own piece")

    if destPiece[0] == currentTurn[0] :
        raise Exception("[WrongMoveException]: Movement can't end on another your own piece ")

    if fromCell == toCell :
        raise Exception("[WrongMoveException]: Empty movement")

    generatorName = selectedPiece[2:].lower() + "Generator"
    module = __import__(generatorName)
    class_ = getattr(module, generatorName[0].upper()+generatorName[1:])
    instance = class_()

    possibleMoves = instance.generateMoves(fromCell)
    res = False

    for move in possibleMoves:
        t = from_matrix_to_chessboard(move)

        if t == toCell:
            print("Correct:",t)
            res = True

    if res == True:
        # Update chessboard
        chessboard.update(fromCell,toCell)
        if destPiece[2:] == "KING":
            print("End game")
            chessboard.setVictory(currentTurn)
        else:
            chessboard.increment_turn()

        return True

    raise Exception("[WrongMoveException]: Wrong move")
