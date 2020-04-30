from tkinter import *
import tkinter as tk
import sys
import os
import signal
import numpy as np
import threading
from threading import Thread
from ctypes import windll
from win32api import GetSystemMetrics
from PIL import Image, ImageTk

sys.path.append("../model/")
from chessboard import *
from executer import *

### THREAD FOR UPDATING
class Thread_Update(Thread):
    def __init__(self, canvas):
        Thread.__init__(self)
        self.canvas = canvas
        self.stop = False

    def run(self):
        print("thread update partito")
        while chessboard.isEnded() != True and self.stop == False :
            event.wait()
            event.clear()
            self.canvas.delete("piece")
            pieces = chessboard.getPieces()
            pieces = np.flip(pieces,1)
            pieces
            for i in range(8):
                for j in range(8):
                    if pieces[i,j] != Piece.EMPTY:
                        img = PIECES[pieces[i,j].name.lower()]
                        self.canvas.create_image(cell_size/2+i*cell_size, cell_size/2+j*cell_size, tags="piece", image=img)

    def terminate(self):
        self.stop = True
        os.kill(os.getpid(), signal.SIGINT)


app = Tk()

### RESOURCES
w_pawn = ImageTk.PhotoImage(file="./resources/gui/whitePawn.png", width=10, height=10)
w_rook = ImageTk.PhotoImage(file="./resources/gui/whiteRook.png", width=10, height=10)
w_knight = ImageTk.PhotoImage(file="./resources/gui/whiteKnight.png", width=10, height=10)
w_bishop = ImageTk.PhotoImage(file="./resources/gui/whiteBishop.png", width=10, height=10)
w_queen = ImageTk.PhotoImage(file="./resources/gui/whiteQueen.png", width=10, height=10)
w_king = ImageTk.PhotoImage(file="./resources/gui/whiteKing.png", width=10, height=10)
b_pawn = ImageTk.PhotoImage(file="./resources/gui/blackPawn.png", width=10, height=10)
b_rook = ImageTk.PhotoImage(file="./resources/gui/blackRook.png", width=10, height=10)
b_knight = ImageTk.PhotoImage(file="./resources/gui/blackKnight.png", width=10, height=10)
b_bishop = ImageTk.PhotoImage(file="./resources/gui/blackBishop.png", width=10, height=10)
b_queen = ImageTk.PhotoImage(file="./resources/gui/blackQueen.png", width=10, height=10)
b_king = ImageTk.PhotoImage(file="./resources/gui/blackKing.png", width=10, height=10)

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

### FUNCTIONS
def doMove():
    print("doMove")
    checkAndExecuteMove("a2", "a3")

chessboard = Chessboard.getInstance()
event = chessboard.getUpdateEvent()

###MAIN APP
def startTkinterApp(init_posx = 0, init_posy = 0, width = 700, height = 700):

    cell_size = int(width/8)

    print("SCREEN RESOLUTION: ", width,height)
    app.title("AR CHESS")
    app.geometry(str(width)+"x"+str(height)+"+"+str(init_posx)+"+"+str(init_posy))
    windll.shcore.SetProcessDpiAwareness(2) ## helps window to look well defined and not blur

    canvas = Canvas(app, width=width, height=height)
    canvas.pack()

    colors = ("white", "gray")
    k = 0
    for i in range(8):
        for j in range(8):
            canvas.create_rectangle(i*cell_size, j*cell_size, (i*cell_size)+cell_size, (j*cell_size+cell_size), fill=colors[k])
            k = (k + 1) % 2

        k = (k + 1) % 2

    pieces = chessboard.getPieces()
    pieces = np.flip(pieces,1)
    for i in range(8):
        for j in range(8):
            if pieces[i,j] != Piece.EMPTY:
                img = PIECES[pieces[i,j].name.lower()]
                canvas.create_image(cell_size/2+i*cell_size, cell_size/2+j*cell_size, tags="piece", image=img)

    t = Thread_Update(canvas)
    t.start()
    app.after(5000, doMove)
    app.mainloop()

    t.terminate()

if __name__ == '__main__':
    startTkinterApp()
