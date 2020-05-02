"""
    Define the abstract class for the Player taxonomy.
"""

from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, role):
        self.name = role

    @abstractmethod
    def doMove(self):
        pass
