from game.tools.constants import *
class Piece():
    def __init__(self, color):
        self.color = color 

    def valid_moves(self, board):
        pass 

    def __repr__(self):
        return "{} {} {}".format(self.__class__, self.color)

    def __str__(self):
        return "{} {} {}".format(self.__class__, self.color)