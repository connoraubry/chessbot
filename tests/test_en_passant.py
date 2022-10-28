import unittest

from game import *

class EnPassantTester(unittest.TestCase):
    def test_start(self):
        g = Gamestate()
        self.assertEqual(g.en_passant, -1)
    def test_e4(self):
        g = Gamestate()
        g.take_move('e4')
        self.assertEqual(g.en_passant, c2idx('e3'))
    def test_e4_e5(self):
        g = Gamestate()
        g.take_move('e4')
        g.take_move('e5')
        self.assertEqual(g.en_passant, c2idx('e6'))
    def test_e4_e5_Nc3(self):
        g = Gamestate()
        g.take_move('e4')
        g.take_move('e5')
        g.take_move('Nc3')
        self.assertEqual(g.en_passant, -1)

    def test_en_passant_in_valid_moves(self):
        g = Gamestate()
        g.take_move('e4')
        g.take_move('a6')

        g.take_move('e5')
        g.take_move('d5')

        moves = g.get_all_moves()

        self.assertTrue('exd6' in moves)

    def test_take_en_passant(self):
        g = Gamestate()
        g.take_move('e4')
        g.take_move('a6')

        g.take_move('e5')
        g.take_move('d5')

        g.take_move('exd6')
        moves = g.get_all_moves()

        self.assertEqual(None, g.board['d5'])
        self.assertEqual(None, g.board['e5'])
        self.assertTrue('exd6' in moves)
        self.assertEqual(Piece('P'), g.board['d6'])