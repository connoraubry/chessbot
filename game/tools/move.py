#start: coordinate of starting move 
#end: coordinate of ending move 
#capture: 0 for no capture, piece if otherwise 
from game.tools.helpers import *
from collections import defaultdict
def default_attack_spot_function(a, b):
    return defaultdict(set)
class Move():
    def __init__(self, start, end, piece, capture,
                    promotion=None, 
                    en_passant_revealed_spot=None, en_passant_piece_spot=None,
                    check=False, checkmate=False,
                    castle=None,
                    attack_spot_function=default_attack_spot_function):
        self.start = start
        self.end = end 
        self.piece = piece
        self.capture = capture

        self.promotion = promotion

        #revelaed on move 
        self.en_passant_revealed_spot = en_passant_revealed_spot

        #this move is actaully an en passant 
        self.en_passant_piece_spot = en_passant_piece_spot

        self.check = check
        self.checkmate = checkmate

        self.castle = castle

        self.attack_spot_function = attack_spot_function

    
    def to_string(self):
        suffix = ''
        if self.check:
            suffix = '+'
        if self.checkmate:
            suffix = '#'


        if self.castle is not None:
            map = {
                'K': 'O-O',
                'k': 'O-O',
                'Q': 'O-O-O',
                'q': 'O-O-O'
            }
            return map[self.castle] + suffix 

        piece = self.piece.to_string().upper()
        piece = self.specify_with_multiple_pieces(piece)

        if self.piece.is_pawn():
            piece = ""
            string = ""
            if self.capture is not None:
                start = index_to_coordinate(self.start)
                end = index_to_coordinate(self.end)
                string = "{}x{}".format(start[0], end)
            if self.promotion is not None:
                if string == "":
                    string = index_to_coordinate(self.end)
                return "{}={}{}".format(string, self.promotion, suffix)
            if string != "":
                return "{}{}".format(string, suffix)
        capture = ""
        if self.capture is not None:
            capture = 'x'
        end = index_to_coordinate(self.end)
        return "{}{}{}{}".format(piece, capture, end, suffix)
    

    def specify_with_multiple_pieces(self, piece):

        if self.piece.piece == PieceName.QUEEN and self.start == 61 and self.end == 54:
            print(self.attack_spot_function(self.end, self.piece.piece))

        canUseFile, canUseRank = True, True 

        source_indicies = self.attack_spot_function(self.end, self.piece.piece)

        if len(source_indicies) < 2:
            return piece

        for source_index in self.attack_spot_function(self.end, self.piece.piece):

            if source_index == self.start:
                continue 
            source_r, source_f = rank_and_file(self.start)
            r, f = rank_and_file(source_index)

            if source_f == f:
                canUseFile = False
            elif source_r == r:
                canUseRank = False 



        if canUseFile:
            piece += index_to_coordinate(self.start)[0]
        elif canUseRank:
            piece += index_to_coordinate(self.start)[1] 
        else:
            piece += index_to_coordinate(self.start)


        return piece 

    def __repr__(self):
        return self.to_string()