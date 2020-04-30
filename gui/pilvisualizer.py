import sys
import cv2
import numpy as np
import time
from PIL import Image

sys.path.append("../model/")
from chessboard import *
from executer import *

### RESOURCES
w_pawn = Image.open("../resources/gui/whitePawn.png")
w_rook = Image.open("../resources/gui/whiteRook.png")
w_knight = Image.open("../resources/gui/whiteKnight.png")
w_bishop = Image.open("../resources/gui/whiteBishop.png")
w_queen = Image.open("../resources/gui/whiteQueen.png")
w_king = Image.open("../resources/gui/whiteKing.png")
b_pawn = Image.open("../resources/gui/blackPawn.png")
b_rook = Image.open("../resources/gui/blackRook.png")
b_knight = Image.open("../resources/gui/blackKnight.png")
b_bishop = Image.open("../resources/gui/blackBishop.png")
b_queen = Image.open("../resources/gui/blackQueen.png")
b_king = Image.open("../resources/gui/blackKing.png")

PIECES = {
"w_pawn": w_pawn,
"w_rook": w_rook,
"w_knight": w_knight,
"w_bishop": w_bishop,
"w_queen": w_queen,
"w_king": w_king,
"b_pawn": b_pawn,
"b_rook": b_rook,
"b_knight": b_knight,
"b_bishop": b_bishop,
"b_queen": b_queen,
"b_king": b_king,
}


if __name__ == '__main__':
    width = 300
    height = 300
    board = Image.open("../resources/gui/board.png")
    board = board.convert("RGB")
    print(board.size)
    cell_size = int(board.size[0]/8)
    print(cell_size)

    ## paste
    # board.paste(w_pawn, (100,100), w_pawn)
    chessboard = Chessboard.getInstance()
    pieces = chessboard.getPieces()
    # pieces = np.flip(pieces,1)
    for i in range(8):
        for j in range(8):
            if pieces[i,j] != Piece.EMPTY:
                img = PIECES[pieces[i,j].name.lower()]
                size = img.size
                cell = (int(cell_size/2+i*cell_size-size[0]/2), int(cell_size/2+j*cell_size-size[1]/2))
                print(cell)
                board.paste(img, (cell[0],cell[1]), img)

    open_cv_image = np.array(board)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    open_cv_image = cv2.resize(open_cv_image, (width, height))

    cv2.imshow("VEDIAMO SE VA", open_cv_image)
    cv2.waitKey(0)
