from tracemalloc import start
import unittest

from game.gamestate import Gamestate
from game.tools.constants import *
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


    def test_export_FEN(self):
        g = Gamestate(fen=starting_FEN)
        new_fen = g.export_FEN()
        self.assertEqual(starting_FEN, new_fen)
    
    def test_export_FEN_middlegame_1(self):
        fen=fen_configs['middlegame_1']
        g = Gamestate(fen)
        self.assertEqual(g.export_FEN(), fen)

    def test_get_all_moves(self):
        g = Gamestate()
        all_moves = g.get_all_moves()
        self.assertSetEqual(all_moves, first_moves)
    

    def test_get_all_moves_e4(self):
        g = Gamestate()
        g.take_move('e4')

        all_moves = g.get_all_moves()
        self.assertSetEqual(all_moves, first_black_moves)


    def test_move_to_start(self):
        g = Gamestate()
        all_moves = g.moves
        self.assertSetEqual(set(g.move_to_start.keys()), g.moves)

    def test_get_move(self):
        g = Gamestate()
        self.assertSetEqual(set(), g.get_move(0))
        self.assertSetEqual(set(), g.get_move(2))
        self.assertSetEqual(set(['Na3', 'Nc3']), g.get_move(1))
        self.assertSetEqual(set(['a3', 'a4']), g.get_move(8))

    def test_take_move(self):
        g = Gamestate()
        g.take_move('e4')
        self.assertEqual(g.board['e2'], None)
        self.assertEqual(g.board['e3'], None)
        self.assertEqual(g.board['e4'], 'P')


