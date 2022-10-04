import unittest

from game.gamestate import Gamestate
from tests.constants import *

class GameTester(unittest.TestCase):
    def test_init(self):
        g = Gamestate()

        self.assertEqual(g.board['a1'], 'R')
        self.assertEqual(g.en_passant, "-")
        self.assertEqual(g.castle, "KQkq")
        self.assertEqual(g.halfmove_clock, 0)
        self.assertEqual(g.fullmove_counter, 1)
        self.assertEqual(g.move, 'w')

    def test_get_all_moves(self):
        g = Gamestate()
        all_moves = g.get_all_moves()
        self.assertSetEqual(all_moves, first_moves)
    
    def test_get_move(self):
        g = Gamestate()
        self.assertSetEqual(set(), g.get_move(0))
        self.assertSetEqual(set(), g.get_move(2))
        self.assertSetEqual(set(['Na3', 'Nc3']), g.get_move(1))
        self.assertSetEqual(set(['a3', 'a4']), g.get_move(8))