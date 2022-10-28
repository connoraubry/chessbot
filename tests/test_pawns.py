import unittest

from game import *
from tests.constants import *



class PawnTester(unittest.TestCase):
    
    def test_capture_and_move(self):
        g = Gamestate(FEN=None)

        g.board[c2idx('e6')] = Piece('P')
        g.board[c2idx('f7')] = Piece('p')
        p_moves = {x.to_string() for x in g.board.get_pawn_moves(c2idx('e6'))}

        expected  = set(['exf7', 'e7'])
        self.assertSetEqual(expected, p_moves)

    def test_capture_and_move_black(self):
        g = Gamestate(FEN=None)
        g.board[c2idx('e6')] = Piece('P')
        g.board[c2idx('f7')] = Piece('p')
        p_moves = {x.to_string() for x in g.board.get_pawn_moves(c2idx('f7'))}
        expected  = set(['fxe6', 'f6', 'f5'])
        self.assertSetEqual(expected, p_moves)
    
    def test_block(self):
        g = Gamestate(FEN=None)
        g.board[c2idx('e6')] = Piece('P')
        g.board[c2idx('e7')] = Piece('p')
        p_moves = {x.to_string() for x in g.board.get_pawn_moves(c2idx('e6'))}
        expected  = set()
        self.assertSetEqual(expected, p_moves)

    def test_start_white(self):
        ranks = 'abcdefgh'
        ends = '34'
        s = '2'
        for r in ranks:
            g = Gamestate()

            start = r+s

            moves = set()
            for e in ends:
                moves.add(r+e)

            p_moves  = {x.to_string() for x in g.board.get_pawn_moves(c2idx(start))}
            self.assertSetEqual(p_moves, moves)
    
    def test_start_black(self):
        ranks = 'abcdefgh'
        ends = '56'
        s = '7'
        for r in ranks:
            g = Gamestate()

            start = r+s

            moves = set()
            for e in ends:
                moves.add(r+e)
            print(g.board)
            p_moves  = {x.to_string() for x in g.board.get_pawn_moves(c2idx(start))}
            self.assertSetEqual(p_moves, moves)
