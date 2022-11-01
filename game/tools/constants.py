from enum import Enum, unique, auto

@unique
class PieceType(Enum):
    PAWN   = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK   = auto()
    QUEEN  = auto() 
    KING   = auto()
    
@unique
class Player(Enum):
    WHITE = auto()
    BLACK = auto()


rank_to_idx = {number: idx for idx, number in enumerate('12345678')}
idx_to_rank = {idx: number for idx, number in enumerate('12345678')}
file_to_idx = {letter: idx for idx, letter in enumerate('abcdefgh')}
idx_to_file = {idx: letter for idx, letter in enumerate('abcdefgh')}

valid_ranks = [number for number in '12345678']
valid_files = [letter for letter in 'abcdefgh']
valid_colors = ['w', 'b']

white_pieces = 'PRNBQK'
black_pieces = 'prnbqk'

valid_pieces = white_pieces + black_pieces
starting_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

piece_to_unicode_dict = {
    'p': '\u265F',
    'n': '\u265E',
    'b': '\u265D',
    'r': '\u265C',
    'q': '\u265B',
    'k': '\u265A',
    'P': '\u2659',
    'N': '\u2658',
    'B': '\u2657',
    'R': '\u2656',
    'Q': '\u2655',
    'K': '\u2654',
    None: '\u00B7'
}

opposite_piece = {
    Player.WHITE: {
        'pawn': 'p',
        'rook': 'r',
        'bishop': 'b',
        'knight': 'n',
        'queen': 'q',
        'king': 'k'
    },
    Player.BLACK: {
        'pawn': 'P',
        'rook': 'R',
        'bishop': 'B',
        'knight': 'N',
        'queen': 'Q',
        'king': 'K'  
    }
}

letter_to_player = {
    'w': Player.WHITE,
    'b': Player.BLACK
}
player_to_letter = {
    Player.WHITE: 'w',
    Player.BLACK: 'b'
}

opponent = {
    Player.WHITE: Player.BLACK,
    Player.BLACK: Player.WHITE
}

letter_to_piece = {
    'P': (PieceType.PAWN, Player.WHITE),
    'N': (PieceType.KNIGHT, Player.WHITE),
    'B': (PieceType.BISHOP, Player.WHITE),
    'R': (PieceType.ROOK, Player.WHITE),
    'Q': (PieceType.QUEEN, Player.WHITE),
    'K': (PieceType.KING, Player.WHITE),
    'p': (PieceType.PAWN, Player.BLACK),
    'n': (PieceType.KNIGHT, Player.BLACK),
    'b': (PieceType.BISHOP, Player.BLACK),
    'r': (PieceType.ROOK, Player.BLACK),
    'q': (PieceType.QUEEN, Player.BLACK),
    'k': (PieceType.KING, Player.BLACK)
}
piece_to_letter = {
    Player.BLACK: {
        PieceType.PAWN: 'p',
        PieceType.KNIGHT: 'n',
        PieceType.BISHOP: 'b',
        PieceType.ROOK: 'r',
        PieceType.QUEEN: 'q',
        PieceType.KING: 'k',
    },
    Player.WHITE: {
        PieceType.PAWN: 'P',
        PieceType.KNIGHT: 'N',
        PieceType.BISHOP: 'B',
        PieceType.ROOK: 'R',
        PieceType.QUEEN: 'Q',
        PieceType.KING: 'K',
    }
}

promotion_pieces = [PieceType.KNIGHT, PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]


castle_int_to_string = {
    0: '-', 1: 'q', 2: 'kq', 3: 'k',
    4: 'Q', 5: 'Qq', 6: 'Qk', 7: 'Qkq',
    8: 'K', 9: 'Kq', 10: 'Kk', 11: 'Kkq',
    12: 'KQ', 13: 'KQq', 14: 'KQk', 15: 'KQkq'
}