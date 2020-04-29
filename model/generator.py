from abc import ABC, abstractmethod

class Generator(ABC):

    @abstractmethod
    def generateMoves(self, fromCell):
        pass
