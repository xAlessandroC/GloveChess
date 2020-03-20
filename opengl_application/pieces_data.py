import os
from objloader_complete import *

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

    print(PIECES_DICT)

if __name__ == "__main__":
    load_pieces()
