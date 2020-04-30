import pygame
from pygame.locals import *
import numpy as np
import sys
import time
relative_path = ".."
sys.path.append(relative_path+"/model/")
from queue import *

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,400)

from chessboard import *
from executer import *

width = 250
height = 250
model = None

mode = "debug"

## LOAD PIECES
board = pygame.image.load(relative_path + "/resources/gui/board.png")
board = pygame.transform.scale(board, (width, height))

pieces_group = pygame.sprite.Group()
w_pawn = pygame.sprite.Sprite(pieces_group);    w_pawn.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/whitePawn.png"),(int(width/8), int(height/8)))
w_rook = pygame.sprite.Sprite(pieces_group);    w_rook.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/whiteRook.png"),(int(width/8), int(height/8)))
w_knight = pygame.sprite.Sprite(pieces_group);  w_knight.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/whiteKnight.png"),(int(width/8), int(height/8)))
w_bishop = pygame.sprite.Sprite(pieces_group);  w_bishop.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/whiteBishop.png"),(int(width/8), int(height/8)))
w_queen = pygame.sprite.Sprite(pieces_group);   w_queen.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/whiteQueen.png"),(int(width/8), int(height/8)))
w_king = pygame.sprite.Sprite(pieces_group);    w_king.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/whiteKing.png"),(int(width/8), int(height/8)))

b_pawn = pygame.sprite.Sprite(pieces_group);    b_pawn.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/blackPawn.png"),(int(width/8), int(height/8)))
b_rook = pygame.sprite.Sprite(pieces_group);    b_rook.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/blackRook.png"),(int(width/8), int(height/8)))
b_knight = pygame.sprite.Sprite(pieces_group);  b_knight.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/blackKnight.png"),(int(width/8), int(height/8)))
b_bishop = pygame.sprite.Sprite(pieces_group);  b_bishop.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/blackBishop.png"),(int(width/8), int(height/8)))
b_queen = pygame.sprite.Sprite(pieces_group);   b_queen.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/blackQueen.png"),(int(width/8), int(height/8)))
b_king = pygame.sprite.Sprite(pieces_group);    b_king.image = pygame.transform.scale(pygame.image.load(relative_path +"/resources/gui/blackKing.png"),(int(width/8), int(height/8)))

pieces = [w_pawn,w_rook,w_knight,w_bishop,w_queen,w_king,
          b_pawn,b_rook,b_knight,b_bishop,b_queen,b_king]

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

centers = []
start = (int(width*0.008),int(height*0.008))
length = 31
count = 0
for i in range(8):
    for j in range(8):
        centers.append((start[0]+i*length,start[1]+j*length))
        count = count + 1

centers = np.array(centers).reshape((8,8,2))

# centers = np.flip(centers, 1)
chessboard = Chessboard.getInstance()

## FUNCTIONS
def loadPieces(screen):
    model = chessboard.getPieces()
    model = np.flip(model,1)

    for i in range(8):
        for j in range(8):
            if model[i,j] != Piece.EMPTY:
                screen.blit(PIECES[model[i,j].name.lower()].image,centers[i,j])

def startGui():
    global model, board

    pygame.init()
    size = (width, height)
    screen = pygame.display.set_mode(size)
    icon = pygame.image.load(relative_path +"/resources/gui/chess.png")
    pygame.display.set_caption("AR Chess")
    pygame.display.set_icon(icon)

    ## BACKGROUND
    background = board

    screen.blit(background,(0,0))
    loadPieces(screen)
    pygame.display.flip()
    print("caricato pezzi")

    event = chessboard.getUpdateEvent()
    print("pygame preso evento")
    while chessboard.isEnded() != True:
        event.wait()
        event.clear()

        print("pygame update chessboard")
        loadPieces(screen)
        print("pygame aggiornato")

        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    startGui()
    print("ciao")

    time.sleep(3)

    checkAndExecuteMove("a2", "a3")
    print("eseguito mossa")
