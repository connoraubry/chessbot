import unittest
import itertools

from game.gamestate import Gamestate
from game.tools import * 
from tests.constants import *
from game.board.piece import *
one_bishop_moves = {
    'a1': set(['Bb2', 'Bc3', 'Bd4', 'Be5', 'Bf6', 'Bg7', 'Bh8']),
    'b2': set(['Ba1', 'Bc3', 'Bd4', 'Be5', 'Bf6', 'Bg7', 'Bh8', 'Ba3', 'Bc1']),
    'c3': set(['Ba1', 'Bb2', 'Bd4', 'Be5', 'Bf6', 'Bg7', 'Bh8', 'Ba5', 'Bb4', 'Bd2', 'Be1']),
    'd4': set(['Ba1', 'Bb2', 'Bc3', 'Be5', 'Bf6', 'Bg7', 'Bh8', 'Ba7', 'Bb6', 'Bc5', 'Be3', 'Bf2', 'Bg1']),
    'e5': set(['Ba1', 'Bb2', 'Bc3', 'Bd4', 'Bf6', 'Bg7', 'Bh8', 'Bb8', 'Bc7', 'Bd6', 'Bf4', 'Bg3', 'Bh2']),
    'f6': set(['Ba1', 'Bb2', 'Bc3', 'Bd4', 'Be5', 'Bg7', 'Bh8', 'Bd8', 'Be7', 'Bg5', 'Bh4']),
    'g7': set(['Ba1', 'Bb2', 'Bc3', 'Bd4', 'Be5', 'Bf6', 'Bh8', 'Bf8', 'Bh6']),
    'h8': set(['Ba1', 'Bb2', 'Bc3', 'Bd4', 'Be5', 'Bf6', 'Bg7']),
}


class BishopTester(unittest.TestCase):
    
    def test_get_move_one_bishop(self):
        for spot, expected in one_bishop_moves.items():
            g = Gamestate(FEN=None)
            g.board[spot] = Piece('B')
            b_moves = {x.to_string() for x in g.board.get_bishop_moves(c2idx(spot))}
            self.assertSetEqual(expected, b_moves)

    def test_capture(self):
        g = Gamestate(FEN=None)
        g.board['a1'] = Piece('B')
        g.board['e5'] = Piece('k')
        b_moves = {x.to_string() for x in g.board.get_bishop_moves(c2idx('a1'))}

        moves = set(['Bb2', 'Bc3', 'Bd4', 'Bxe5'])
        self.assertSetEqual(moves, b_moves)