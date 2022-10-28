from game.tools.constants import * 

class Piece():
    def __init__(self, letter=None, pieceName=None, player=None):
        if letter == pieceName == player == None:
            raise ValueError
        if letter is not None:
            self.piece, self.player = letter_to_piece[letter]
        else:
            self.piece = pieceName
            self.player = player


    def is_pawn(self):
        return self.piece == PieceName.PAWN
    def is_knight(self):
        return self.piece == PieceName.KNIGHT
    def is_bishop(self):
        return self.piece == PieceName.BISHOP
    def is_rook(self):
        return self.piece == PieceName.ROOK
    def is_queen(self):
        return self.piece == PieceName.QUEEN
    def is_king(self):
        return self.piece == PieceName.KING

    def is_white(self):
        return self.player == Player.WHITE
    def is_black(self):
        return self.player == Player.BLACK

    def __eq__(self, opposite):
        if opposite == None:
            return False 
        return self.piece == opposite.piece and self.player == opposite.player

    def to_string(self):
        return piece_to_letter[self.player][self.piece]

    def __repr__(self):
        return self.to_string()

def get_opposite_piece(player, piece):
    if player == None:
        return None 
    return Piece(opposite_piece[player][piece])

def piece_to_unicode(piece):
    if piece == None:
        return piece_to_unicode_dict[piece]
    return piece_to_unicode_dict[piece.to_string()]