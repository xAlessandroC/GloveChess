from player import *

class IAPlayer(Player):

    def __init__(self, role):
        self.name = role

    def doMove(self):
        print("ciao IA")
