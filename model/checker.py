from abc import ABC, abstractmethod

class Checker(ABC):

    @abstractmethod
    def checkMove(self, fromCell, toCell):
        pass
