class Node():

    def __init__(self, state, value = None, action = None):
        self.__state = state
        self.__value = value
        self.__action = action

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
