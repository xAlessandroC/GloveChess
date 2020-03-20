import sys
sys.path.append('../model/')
sys.path.append('../')

from chessboard import *
# from executer import *
# from guiVisualizer import *
from player import *
from threading import Thread
import threading
import time
from ARChess_application import *

_chessboard = Chessboard.getInstance()
lock = threading.RLock()
condition = threading.Condition(lock)

if __name__ == "__main__":
    _chessboard = Chessboard.getInstance()
    playerW = Players("WHITE")
    playerB = Players("BLACK")
    main = AR()

    playerW.start()
    playerB.start()
    main.start()
