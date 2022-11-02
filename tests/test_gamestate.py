import unittest

from game import * 
from tests.constants import *

class GameTester(unittest.TestCase):
    def test_init(self):
        g = Gamestate()

        self.assertEqual(g.board['a1'].to_string(), 'R')
        self.assertEqual(g.en_passant, -1)
        self.assertEqual(g.castle, "KQkq")
        self.assertEqual(g.halfmove_clock, 0)
        self.assertEqual(g.fullmove_counter, 1)
        self.assertEqual(g.move, Player.WHITE)

    def test_export_FEN(self):
        g = Gamestate(FEN=starting_FEN)
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

    def test_get_move(self):
        g = Gamestate()
        self.assertSetEqual(set(), {x.to_string() for x in g.get_move(0)[0]})
        self.assertSetEqual(set(), {x.to_string() for x in g.get_move(2)[0]})
        self.assertSetEqual(set(['Na3', 'Nc3']), {x.to_string() for x in g.get_move(1)[0]})
        self.assertSetEqual(set(['a3', 'a4']), {x.to_string() for x in g.get_move(8)[0]})

    def test_take_move(self):
        g = Gamestate()
        g.take_move('e4')
        self.assertEqual(g.board['e2'], None)
        self.assertEqual(g.board['e3'], None)
        self.assertEqual(g.board['e4'].to_string(), 'P')

    def test_pawn_under_attack(self):
        g = Gamestate()
        g.take_move('e4')
        self.assertEqual(g.fullmove_counter, 1)
        g.take_move('d5')
        self.assertEqual(g.fullmove_counter, 2)
        self.assertEqual(g.halfmove_clock, 0)
        self.assertTrue('exd5' in g.get_all_moves())

        g.take_move('Nc3')
        self.assertEqual(g.fullmove_counter, 2)
        self.assertEqual(g.halfmove_clock, 1)
    