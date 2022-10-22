import unittest 
from game.board.board import Board 
from game.tools import *
from tests.constants import *

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
        self.assertEqual(b['a1'], 'R')
        self.assertEqual(b['d1'], 'Q')
        self.assertEqual(b.white_king, 'e1')
        self.assertEqual(b.black_king, 'e8')

    def test_export_FEN(self):
        positions = starting_FEN.split(" ")[0]
        b = Board(FEN_positions=positions)
        new_positions = b.export_board_to_FEN_positions()
        self.assertEqual(positions, new_positions)

    def test_export_FEN_e4(self):
        positions = fen_configs['e4'].split(" ")[0]
        b = Board(FEN_positions=positions)
        new_positions = b.export_board_to_FEN_positions()
        self.assertEqual(positions, new_positions)

    def test_export_FEN_giuoco_piano(self):
        positions = fen_configs['giuoco_piano'].split(" ")[0]
        b = Board(FEN_positions=positions)
        new_positions = b.export_board_to_FEN_positions()
        self.assertEqual(positions, new_positions)

    def test_export_FEN_middlegame_1(self):
        positions = fen_configs['middlegame_1'].split(" ")[0]
        b = Board(FEN_positions=positions)
        new_positions = b.export_board_to_FEN_positions()
        self.assertEqual(positions, new_positions)

    def test_iter(self):
        positions = starting_FEN.split(" ")[0]
        b = Board(FEN_positions=positions)
        for piece in b:
            self.assertTrue(piece is None or piece in valid_pieces)

    def test_under_attack_knight(self):
        b = Board()
        b['a1'] = 'K'
        b['b3'] = 'n'

        for piece, eval in zip(['n', 'q', 'r', 'p', 'b'], \
                                [True, False, False, False, False]):
            b['b3'] = piece 

            a1_index = coordinate_to_index('a1')
            b3_index = coordinate_to_index('b3')
            self.assertEqual(b.piece_under_attack(a1_index), eval)
            self.assertFalse(b.piece_under_attack(b3_index))

    def test_under_attack_bishop(self):
        b = Board()
        b['a1'] = 'K'

        for piece, eval in zip(['n', 'q', 'r', 'p', 'b'], \
                                [False, True, False, False, True]):
            b['c3'] = piece 
            print(piece)
            self.assertEqual(b.piece_under_attack(coordinate_to_index('a1')), eval)
            self.assertFalse(b.piece_under_attack(coordinate_to_index('c3')))

    def test_under_attack_rook(self):
        b = Board()
        b['a1'] = 'K'

        for spot in ['c1', 'd1', 'e1', 'f1', 'a3', 'a4', 'a5', 'a6']:
            for piece, eval in zip(['n', 'q', 'r', 'p', 'b'], \
                                    [False, True, True, False, False]):
                b[spot] = piece 
                spot_index = coordinate_to_index(spot)
                self.assertEqual(b.piece_under_attack(0), eval)
                self.assertFalse(b.piece_under_attack(spot_index))
                b[spot] = None

    def test_under_attack_rook_two(self):
        b = Board()
        b['a1'] = 'K'
        b['a3'] = 'r'
        self.assertTrue(b.piece_under_attack(coordinate_to_index('a1')))

    def test_under_attack_king(self):
        b = Board()
        b['c3'] = 'p'

        for kingspot in ['c4', 'c2', 'b3', 'b4', 'b2', 'd3', 'd2', 'd4']:
            b[kingspot] = 'K'
            self.assertTrue(b.piece_under_attack(coordinate_to_index('c3')))
            b[kingspot] = None

    def test_under_attack_pawn_white_king(self):
        b = Board()
        b['c3'] = 'K'
        for pawn_spot, eval in zip(['b2', 'c2', 'd2', 'e2', 'b3', 'b4', 'c4', 'd4'],
                                    [False, False, False, False, False, True, False, True]):
            b[pawn_spot] = 'p'
            self.assertEqual(b.piece_under_attack(coordinate_to_index('c3')), eval)
            b[pawn_spot] = None
    def test_under_attack_pawn_black_king(self):
        b = Board()
        b['c3'] = 'k'
        for pawn_spot, eval in zip(['b2', 'c2', 'd2', 'e2', 'b3', 'b4', 'c4', 'd4'],
                                    [True, False, True, False, False, False, False, False]):
            b[pawn_spot] = 'P'
            index = coordinate_to_index('c3')
            self.assertEqual(b.piece_under_attack(index), eval)
            b[pawn_spot] = None

    def test_under_attack_pawn_white_king(self):
        b = Board()
        b['c3'] = 'K'
        b['d4'] = 'p'
        self.assertTrue(b.piece_under_attack(coordinate_to_index('c3')))
