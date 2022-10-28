from enum import Enum, unique, auto

@unique
class PieceName(Enum):
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

enemy = {
    'w': 'b',
    'b': 'w'
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
    'P': (PieceName.PAWN, Player.WHITE),
    'N': (PieceName.KNIGHT, Player.WHITE),
    'B': (PieceName.BISHOP, Player.WHITE),
    'R': (PieceName.ROOK, Player.WHITE),
    'Q': (PieceName.QUEEN, Player.WHITE),
    'K': (PieceName.KING, Player.WHITE),
    'p': (PieceName.PAWN, Player.BLACK),
    'n': (PieceName.KNIGHT, Player.BLACK),
    'b': (PieceName.BISHOP, Player.BLACK),
    'r': (PieceName.ROOK, Player.BLACK),
    'q': (PieceName.QUEEN, Player.BLACK),
    'k': (PieceName.KING, Player.BLACK)
}
piece_to_letter = {
    Player.BLACK: {
        PieceName.PAWN: 'p',
        PieceName.KNIGHT: 'n',
        PieceName.BISHOP: 'b',
        PieceName.ROOK: 'r',
        PieceName.QUEEN: 'q',
        PieceName.KING: 'k',
    },
    Player.WHITE: {
        PieceName.PAWN: 'P',
        PieceName.KNIGHT: 'N',
        PieceName.BISHOP: 'B',
        PieceName.ROOK: 'R',
        PieceName.QUEEN: 'Q',
        PieceName.KING: 'K',
    }
}

promotion_pieces = [PieceName.KNIGHT, PieceName.BISHOP, PieceName.ROOK, PieceName.QUEEN]