import unittest

from game.gamestate import Gamestate
from game.tools import * 
from tests.constants import *
from game.board.piece import *


class PieceTester(unittest.TestCase):

    def test_get_opposite_piece_knight(self):
        opposite = get_opposite_piece(Player.WHITE, 'knight')
        self.assertEqual(Piece('n'), opposite)
    def test_get_opposite_piece_knight_black(self):
        opposite = get_opposite_piece(Player.BLACK, 'knight')
        self.assertEqual(Piece('N'), opposite)    
    def test_get_opposite_piece_knight_none(self):
        opposite = get_opposite_piece(Player.BLACK, 'knight')
        self.assertNotEqual(None, opposite)
        opposite = get_opposite_piece(Player.WHITE, 'knight')
        self.assertNotEqual(None, opposite)     

    def test_get_opposite_piece_bishop(self):
        opposite = get_opposite_piece(Player.WHITE, 'bishop')
        self.assertEqual(Piece('b'), opposite)
    def test_get_opposite_piece_bishop_black(self):
        opposite = get_opposite_piece(Player.BLACK, 'bishop')
        self.assertEqual(Piece('B'), opposite)    
    def test_get_opposite_piece_bishop_none(self):
        opposite = get_opposite_piece(Player.BLACK, 'bishop')
        self.assertNotEqual(None, opposite)
        opposite = get_opposite_piece(Player.WHITE, 'bishop')
        self.assertNotEqual(None, opposite) 

    def test_get_opposite_piece_rook(self):
        opposite = get_opposite_piece(Player.WHITE, 'rook')
        self.assertEqual(Piece('r'), opposite)
    def test_get_opposite_piece_rook_black(self):
        opposite = get_opposite_piece(Player.BLACK, 'rook')
        self.assertEqual(Piece('R'), opposite)    
    def test_get_opposite_piece_rook_none(self):
        opposite = get_opposite_piece(Player.BLACK, 'rook')
        self.assertNotEqual(None, opposite)
        opposite = get_opposite_piece(Player.WHITE, 'rook')
        self.assertNotEqual(None, opposite)    