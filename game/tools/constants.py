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

piece_to_unicode = {
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
    'w': {
        'pawn': 'p',
        'rook': 'r',
        'bishop': 'b',
        'knight': 'n',
        'queen': 'q',
        'king': 'k'
    },
    'b': {
        'pawn': 'P',
        'rook': 'R',
        'bishop': 'B',
        'knight': 'N',
        'queen': 'Q',
        'king': 'K'  
    }
}