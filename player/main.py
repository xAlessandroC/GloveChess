import sys
sys.path.append('../model/')

from chessboard import *
# from guiVisualizer import *
from player import *
from threading import Thread
import threading
import time

_chessboard = Chessboard.getInstance()
lock = threading.RLock()
condition = threading.Condition(lock)

if __name__ == "__main__":
    _chessboard = Chessboard.getInstance()
    playerW = Player("WHITE")
    playerB = Player("BLACK")

    playerW.start()
    playerB.start()
