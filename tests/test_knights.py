import itertools
import unittest
import itertools

from game.gamestate import Gamestate
from game.tools import * 
from tests.constants import *
from game.board.piece import Piece


one_knight_moves = {
    'a1': set(["Nc2", "Nb3"]),
    'a2': set(["Nc3", "Nb4", "Nc1"]),
    'a3': set(["Nc4", "Nb5", "Nc2", "Nb1"]),
    'b1': set(["Na3", "Nc3", "Nd2"]),
    'b2': set(["Na4", "Nc4", "Nd3", "Nd1"]),
    'b3': set(["Na5", "Na1", "Nc5", "Nc1", "Nd4", "Nd2"]),
    'c1': set(["Na2", "Nb3", "Nd3", "Ne2"]),
    'c2': set(["Na3", "Na1", "Nb4", "Nd4", "Ne3", "Ne1"]),
    'c3': set(["Na4", "Na2", "Nb5", "Nd5", "Nb1", "Nd1", "Ne4", "Ne2"]),
    'a8': set(["Nb6", "Nc7"]),
    'h8': set(["Ng6", "Nf7"])
}

def setup_num_moves_by_space():
    num_moves_by_space = {}

    for r in itertools.product(valid_files, valid_ranks):
        coordinate = r[0] + r[1]
        rank = rank_to_idx[r[1]]
        file = file_to_idx[r[0]]

        if 2 <= file <= 5 and 2 <= rank <= 5:
            num_moves_by_space[coordinate] = 8

        if file == 1 or file == 6 or rank == 1 or rank == 6:
            num_moves_by_space[coordinate] = 6

        if (file == 1 or file == 6) and (rank == 1 or rank == 6):
            num_moves_by_space[coordinate] = 4

        if file == 0 or file == 7 or rank == 0 or rank == 7:
            num_moves_by_space[coordinate] = 4

        if (file == 0 or file == 7) and (rank == 0 or rank == 7):
            num_moves_by_space[coordinate] = 2
    num_moves_by_space['a2'] = 3
    num_moves_by_space['a7'] = 3
    num_moves_by_space['b1'] = 3
    num_moves_by_space['b8'] = 3

    num_moves_by_space['h2'] = 3
    num_moves_by_space['h7'] = 3
    num_moves_by_space['g1'] = 3
    num_moves_by_space['g8'] = 3

    return num_moves_by_space
num_moves_by_space = setup_num_moves_by_space()

class KnightTester(unittest.TestCase):
    
    def test_get_move_one_knight(self):
        for spot, expected in one_knight_moves.items():
            g = Gamestate(FEN=None)
            g.board[spot] = Piece('N')
            self.assertSetEqual(expected, g.get_move(spot))

    def test_one_knight_num_moves(self):
        for spot, num_moves in num_moves_by_space.items():
            g = Gamestate(FEN=None)
            g.board[spot] = Piece("N")
            self.assertEqual(len(g.get_move(spot)), num_moves)

    def test_one_knight_captures(self):
        g = Gamestate(FEN=None)
        g.board['a1'] = Piece("N")
        g.board['b3'] = Piece('p')
        self.assertEqual(g.get_move('a1'), {'Nc2', 'Nxb3'})