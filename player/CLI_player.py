"""
    This class define the Command Line Interface player
"""

from player import *
from chessboard import *
from executer import *
from minmax import *

class CLIPlayer(Player):

    def __init__(self, role):
        self.name = role

    def doMove(self):
        result = False
        while result == False:
            from_ = input("Please enter from value:\n")
            to_ = input("Please enter to value:\n")

            try:
                checkAndExecuteMove(from_, to_)
                result = True
            except:
                result = False
                pass
