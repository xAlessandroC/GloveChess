import sys
sys.path.append('../model/')
sys.path.append('../gui/')

from chessboard import *
from executer import *
from guiVisualizer import *
from player import *
from threading import Thread
import time

_chessboard = Chessboard.getInstance()


playerW = Thread(target=startPlayer, args=("WHITE",))
playerB = Thread(target=startPlayer, args=("BLACK",))
gui = Thread(target=startGui)

gui.start()
playerW.start()
playerB.start()
