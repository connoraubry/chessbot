import unittest


import unittest 
from game import *
from tests.constants import * 


class CastleTester(unittest.TestCase):
    def test_oo(self):
        fen = fen_configs['white_oo']
        g = Gamestate(fen)
        moves = g.get_all_moves()
        print(moves)
        self.assertTrue('O-O' in moves)
    def test_oo_invalid(self):
        fen = fen_configs['white_oo_invalid']
        g = Gamestate(fen)
        moves = g.get_all_moves()
        print(moves)
        self.assertFalse('O-O' in moves)

    def test_oo_live(self):
        g = Gamestate()
        g.take_move('e4')
        g.take_move('e5')

        g.take_move('Nf3')
        g.take_move('Nc6')

        g.take_move('Bc4')
        g.take_move('Nf6')

        g.take_move('O-O')

        self.assertEqual(g.board[4], None)
        self.assertEqual(g.board[5], Piece('R'))
        self.assertEqual(g.board[6], Piece('K'))
        self.assertEqual(g.board[7], None)
        self.assertEqual(g.castle, 'kq')


    def test_oo_live_black(self):
        g = Gamestate()
        g.take_move('e4')
        g.take_move('e5')

        g.take_move('Nf3')
        g.take_move('Nf6')

        g.take_move('Bc4')
        g.take_move('Bc5')

        g.take_move('O-O')
        g.take_move('O-O')
        g.print_board()
        self.assertEqual(g.board[60], None)
        self.assertEqual(g.board[61], Piece('r'))
        self.assertEqual(g.board[62], Piece('k'))
        self.assertEqual(g.board[63], None)
        self.assertEqual(g.castle, '')


    def test_ooo_live(self):
        g = Gamestate()
        g.take_move('e3')
        g.take_move('e6')

        g.take_move('Qe2')
        g.take_move('Qe7')

        g.take_move('d3')
        g.take_move('d6')

        g.take_move('Bd2')
        g.take_move('Bd7')

        g.take_move('Nc3')
        g.take_move('Nc6')

        g.take_move('O-O-O')

        self.assertEqual(g.board[4], None)
        self.assertEqual(g.board[3], Piece('R'))
        self.assertEqual(g.board[2], Piece('K'))
        self.assertEqual(g.board[0], None)
        self.assertEqual(g.castle, 'kq')

    def test_ooo_live(self):
        g = Gamestate()
        g.take_move('e3')
        g.take_move('e6')

        g.take_move('Qe2')
        g.take_move('Qe7')

        g.take_move('d3')
        g.take_move('d6')

        g.take_move('Bd2')
        g.take_move('Bd7')

        g.take_move('Nc3')
        g.take_move('Nc6')

        g.take_move('O-O-O')
        g.take_move('O-O-O')

        self.assertEqual(g.board[60], None)
        self.assertEqual(g.board[59], Piece('r'))
        self.assertEqual(g.board[58], Piece('k'))
        self.assertEqual(g.board[57], None)
        self.assertEqual(g.castle, '')