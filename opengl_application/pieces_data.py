import os
from objloader_complete import *
from chessboard import *
from opengl_utils import *
import glut_application as glta

## PIECES
PIECES_CONV = {
"W_KING" : "Re_Bianco",
"W_QUEEN" : "Regina_Bianca",
"W_ROOK" : "Torre_Bianca",
"W_BISHOP" : "Alfiere_Bianco",
"W_KNIGHT" : "Cavallo_Bianco",
"W_PAWN" : "Pedone_Bianco",
"B_KING" : "Re_Nero",
"B_QUEEN" : "Regina_Nera",
"B_ROOK" : "Torre_Nera",
"B_BISHOP" : "Alfiere_Nero",
"B_KNIGHT" : "Cavallo_Nero",
"B_PAWN" : "Pedone_Nero",
}
PIECES_DICT = {}
PIECES_POSITION = {}
id_chessboardList = None
id_selectionSprite = None

def load_pieces():

    path = os.getcwd()[:(os.getcwd().find("AR_Chess")+len("AR_Chess"))]
    os.chdir(path)
    print(os.getcwd())

    directory = r"resources\chess_models_reduced"

    print("Loading pieces...")
    for piece in os.listdir(directory):
        # print(piece)
        piece_dir = directory + "\\" + piece
        for file in os.listdir(piece_dir):
            if file.startswith(piece) and file.endswith(".obj"):
                print("Loading "+piece+"...")
                complete_path = (os.path.join(piece_dir, file)).replace("\\","/")
                print(complete_path)
                obj = OBJ(complete_path)

                PIECES_DICT[piece] = obj

    PIECES_DICT["Puntatore"] = OBJ("resources/chess_models_reduced/Selection/selector.obj")
    print(PIECES_DICT)

def init_piece(centers):
    global id_selectionSprite, id_chessboardList

    _chessboard = Chessboard.getInstance()
    pieces = _chessboard.getPieces()
    print("DICT:",PIECES_DICT)

    ## Carico pezzi scacchi
    for i in range(8):
        for j in range(8):
            if pieces[i,j] != Piece.EMPTY:
                id = glGenLists(1)
                PIECES_POSITION[str(i)+"-"+str(j)] = id
                obj = PIECES_DICT[PIECES_CONV[pieces[i,j].name]]
                print("INDEX:",i,j)
                new_vertices = translateVertices(id, obj, *tuple(centers[i,j]), z=2)
                overwriteList(id, obj, new_vertices)

    ## Carico scacchiera
    id_chessboardList = glGenLists(1)
    obj = PIECES_DICT["Scacchiera"]
    overwriteList(id_chessboardList, obj, obj.vertices)

    ## Carico puntatore per la selezione
    id_selectionSprite = glGenLists(1)
    glta.obj_s = PIECES_DICT["Puntatore"]
    new_vertices = translateVertices(id_selectionSprite, glta.obj_s, *tuple(centers[0,0]), z=13)
    overwriteList(id_selectionSprite, glta.obj_s, new_vertices)

if __name__ == "__main__":
    load_pieces()
