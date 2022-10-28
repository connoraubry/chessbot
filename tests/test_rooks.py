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
    
    def test_get_move_one_rook(self):
        for spot, expected in one_rook_moves.items():
            g = Gamestate(FEN=None)
            g.board[spot] = Piece('R')
            self.assertSetEqual(expected, {x.to_string() for x in g.board.get_rook_moves(c2idx(spot))})

    def test_capture(self):
        g = Gamestate(FEN=None)
        g.board['a5'] = Piece('R')
        g.board['e5'] = Piece('k')
        moves = {x.to_string() for x in g.board.get_rook_moves(c2idx('a5'))}

        expected = set(['Ra1', 'Ra2', 'Ra3', 'Ra4', 'Ra6', 'Ra7', 'Ra8',
                         'Rb5', 'Rc5', 'Rd5', 'Rxe5'])
        self.assertSetEqual(moves, expected)