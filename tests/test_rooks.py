import unittest
import itertools

from game.gamestate import Gamestate
from game.board.piece import Piece
from game.tools import * 
from tests.constants import *

one_rook_moves = {
    'a1': set(['Ra{}'.format(i) for i in range(2, 9)] + ['R{}1'.format(letter) for letter in 'bcdefgh']),
    'b1': set(['Rb{}'.format(i) for i in range(2, 9)] + ['R{}1'.format(letter) for letter in 'acdefgh']),
    'c1': set(['Rc{}'.format(i) for i in range(2, 9)] + ['R{}1'.format(letter) for letter in 'abdefgh']),
    'c4': set(['Rc{}'.format(i) for i in "1235678"] + ['R{}4'.format(letter) for letter in 'abdefgh'])
}

class RookTester(unittest.TestCase):
    
    def test_get_move_one_knight(self):
        for spot, expected in one_rook_moves.items():
            g = Gamestate(FEN=None)
            g.board[spot] = Piece('R')
            self.assertSetEqual(expected, g.get_move(spot))
