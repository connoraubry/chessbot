import itertools
import unittest
import itertools

from game.gamestate import Gamestate
from game.tools import * 
from tests.constants import *

one_king_moves = {
    'a1': {'Ka2', 'Kb1', 'Kb2'},
    'b1': {'Ka1', 'Ka2', 'Kb2', 'Kc1', 'Kc2'},
    'd3': {'Kd2', 'Kd4', 'Kc2', 'Kc3', 'Kc4', 'Ke2', 'Ke3', 'Ke4'}
}

class KingTester(unittest.TestCase):
    
    def test_get_move_one_knight(self):
        for spot, expected in one_king_moves.items():
            g = Gamestate(fen=None)
            g.board[spot] = 'K'
            self.assertSetEqual(expected, g.get_move(spot))
