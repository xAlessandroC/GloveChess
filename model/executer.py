from Chessboard import *
from model_utils import *
from queenChecker import *

def checkAndExecuteMove(fromCell, toCell):
    chessboard = Chessboard.getInstance()

    currentTurn = Player(chessboard.get_turn()[1]).name
    selectedPiece = chessboard.from_index_to_piece(fromCell)

    #Controllo che venga mosso un pezzo del giocatore di cui è il turno
    print("### EXECUTER ###\nCurrent Turn:",currentTurn,"\nSelectedPiece:", selectedPiece)
    print("Chessboard from:", fromCell,"\nMatrix from:",chessboard.from_chessboard_to_matrix(fromCell))
    print("Chessboard to:", toCell,"\nMatrix to:",chessboard.from_chessboard_to_matrix(toCell))

    if selectedPiece[0] != currentTurn[0] :
        raise Exception("[WrongTurnException]: Non stai muovendo un tuo pezzo")

    if fromCell == toCell :
        raise Exception("[WrongMoveException]: Non stai muovendo niente")

    #Controllo che il pezzo rispetti le proprie regole
    checkerName = selectedPiece[2:].lower() + "Checker"
    module = __import__(checkerName)
    class_ = getattr(module, checkerName[0].upper()+checkerName[1:])
    instance = class_()

    if instance.checkMove(fromCell, toCell):
        ##Aggiorno chessboard
        chessboard.update(fromCell,toCell)
        return True


Chessboard.getInstance()
print(checkAndExecuteMove("c2","c1"))
