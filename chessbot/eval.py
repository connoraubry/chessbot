from game import *

piece_to_score = {
    None: 0,
    'K': 20000,
    'Q': 900,
    'R': 500,
    'B': 330,
    'N': 320,
    'P': 100,
    'k': -20000,
    'q': -900,
    'r': -500,
    'b': -330,
    'n': -320,
    'p': -100,

}

def calculate_score(gs):
    score = 0
    for piece in gs.board:
        if piece is not None:
            score += piece_to_score[piece.to_string()]
    return score 