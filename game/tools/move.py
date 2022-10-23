#start: coordinate of starting move 
#end: coordinate of ending move 
#capture: 0 for no capture, piece if otherwise 
from operator import index
from game.tools.helpers import *
class Move():
    def __init__(self, start, end, piece, capture):
        self.start = start
        self.end = end 
        self.piece = piece
        self.capture = capture

    def to_string(self):
        piece = self.piece.to_string().upper()
        if self.piece.is_pawn():
            piece = ""
            if self.capture is not None:
                start = index_to_coordinate(self.start)
                end = index_to_coordinate(self.end)
                return "{}x{}".format(start[0], end)
        capture = ""
        if self.capture is not None:
            capture = 'x'
        end = index_to_coordinate(self.end)
        return "{}{}{}".format(piece, capture, end)
    
    def __repr__(self):
        return self.to_string()