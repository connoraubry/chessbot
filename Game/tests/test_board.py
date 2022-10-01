from operator import pos
from turtle import position
import unittest 
from game.board.board import Board 
from game.tools import *


class BoardTester(unittest.TestCase):

    def test_load_empty_board(self):
        b = Board()
        initBoard = b.board
        self.assertEqual(b['d1'], initBoard[3])
        self.assertEqual(b['a1'], initBoard[0])

    def test_getter(self):
        b = Board()
        b.board[0] = 'test'
        self.assertEqual(b['a1'], 'test')

    def test_setter(self):
        b = Board()
        b['a1'] = 'test'
        self.assertEqual(b.board[0], 'test')

        b['d3'] = 'test'
        self.assertEqual(b.board[19], 'test')

    def test_load_FEN(self):
        positions = starting_FEN.split(" ")[0]
        b = Board(FEN_positions=positions)
    
    def test_iter(self):
        positions = starting_FEN.split(" ")[0]
        b = Board(FEN_positions=positions)
        for piece in b:
            self.assertTrue(piece is None or piece in valid_pieces)
