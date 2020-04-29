class Action():

    def __init__(self, from_, to_):
        self.__from = from_
        self.__to = to_

    def setFrom(self, from_):
        self.__from = from_

    def getFrom(self):
        return self.__from

    def setTo(self, to_):
        self.__to = to

    def getTo(self):
        return self.__to
