#start: coordinate of starting move 
#end: coordinate of ending move 
#capture: 0 for no capture, piece if otherwise 
from game.tools.helpers import *
class Move():
    def __init__(self, start, end, piece, capture):
        self.start = start
        self.end = end 
        self.piece = piece
        self.capture = capture

    def to_string(self):
        piece = self.piece.upper()
        if piece == 'P':
            piece = ""
        capture = ""
        if self.capture is not None:
            capture = 'x'
        end = index_to_coordinate(self.end)
        return "{}{}{}".format(piece, capture, end)