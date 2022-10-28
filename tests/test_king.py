import unittest

from game import *
from tests.constants import *

one_king_moves = {
    'a1': {'Ka2', 'Kb1', 'Kb2'},
    'b1': {'Ka1', 'Ka2', 'Kb2', 'Kc1', 'Kc2'},
    'd3': {'Kd2', 'Kd4', 'Kc2', 'Kc3', 'Kc4', 'Ke2', 'Ke3', 'Ke4'}
}

class KingTester(unittest.TestCase):
    
    def test_get_move_one_king(self):
        for spot, expected in one_king_moves.items():
            g = Gamestate(FEN=None)
            g.board[spot] = Piece('K')
            self.assertSetEqual(expected, {x.to_string() for x in g.get_king_moves(c2idx(spot))})

