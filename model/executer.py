from chessboard import *
from model_utils import *

def checkAndExecuteMove(fromCell, toCell):
    chessboard = Chessboard.getInstance()

    currentTurn = Turn(chessboard.get_turn()[1]).name
    selectedPiece = chessboard.from_index_to_piece(fromCell)
    destPiece = chessboard.from_index_to_piece(toCell)

    #Controllo che venga mosso un pezzo del giocatore di cui è il turno
    print("### EXECUTER ###\nCurrent Turn:",currentTurn,"\nSelectedPiece:", selectedPiece)
    print("Chessboard from:", fromCell,"\nMatrix from:",from_chessboard_to_matrix(fromCell))
    print("Chessboard to:", toCell,"\nMatrix to:",from_chessboard_to_matrix(toCell))

    if selectedPiece[0] != currentTurn[0] :
        raise Exception("[WrongTurnException]: Non stai muovendo un tuo pezzo")

    if destPiece[0] == currentTurn[0] :
        raise Exception("[WrongMoveException]: Il movimento non può terminare su un tuo pezzo")

    if fromCell == toCell :
        raise Exception("[WrongMoveException]: Non stai muovendo niente")

    #Controllo che il pezzo rispetti le proprie regole
    generatorName = selectedPiece[2:].lower() + "Generator"
    module = __import__(generatorName)
    class_ = getattr(module, generatorName[0].upper()+generatorName[1:])
    instance = class_()

    possibleMoves = instance.generateMoves(fromCell)
    res = False
    # print("MOVES:", possibleMoves)
    for move in possibleMoves:
        t = from_matrix_to_chessboard(move)
        # print("MOVE: ",t)
        if t == toCell:
            print("CORRETTA:",t)
            res = True

    if res == True:
        ##Aggiorno chessboard
        chessboard.update(fromCell,toCell)
        if destPiece[2:] == "KING":
            print("Fine partita")
            chessboard.setVictory(currentTurn)
        else:
            chessboard.increment_turn()

        return True
