"""
    Define the abstract class for the Generator taxonomy.
"""

from abc import ABC, abstractmethod

class Generator(ABC):

    @abstractmethod
    def generateMoves(self, fromCell):
        pass
