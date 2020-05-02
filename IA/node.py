"""
    Define the structure of a node of the tree.
"""

class Node():

    def __init__(self, state, value = None, action = None):
        self.__state = state    # state of the chessboard
        self.__value = value    # heuristic value
        self.__action = action  # action which comes from

    def setState(self, state):
        self.__state = state

    def getState(self):
        return self.__state

    def setValue(self, value):
        self.__value = value

    def getValue(self):
        return self.__value

    def setAction(self, action):
        self.__action = action

    def getAction(self):
        return self.__action
