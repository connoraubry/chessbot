import unittest 
from game import *
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
        self.assertEqual(b['a1'].to_string(), 'R')
        self.assertEqual(b['d1'].to_string(), 'Q')
        self.assertEqual(b.white_king, 4)
        self.assertEqual(b.black_king, 60)

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
            self.assertTrue(piece is None or piece.to_string() in valid_pieces)

    def test_under_attack_knight(self):
        b = Board()
        b['a1'] = Piece('K')

        for piece, eval in zip(['n', 'q', 'r', 'p', 'b'], \
                                [True, False, False, False, False]):
            b['b3'] = Piece(piece)

            a1_index = c2idx('a1')
            b3_index = c2idx('b3')

            player = b[a1_index].player
            self.assertEqual(b.piece_under_attack_by_knight(a1_index, player), eval)
            self.assertFalse(b.piece_under_attack_by_knight(b3_index, b[b3_index].player))

    def test_under_attack_bishop(self):
        b = Board()
        b['a1'] = Piece('K')

        for piece, eval in zip(['n', 'q', 'r', 'p', 'b'], \
                                [False, True, False, False, True]):
            b['c3'] = Piece(piece)
            self.assertEqual(b.piece_under_attack_diagonal(c2idx('a1'), b['a1'].player), eval)
            self.assertFalse(b.piece_under_attack_diagonal(c2idx('c3'), b['c3'].player))

    def test_under_attack_rook(self):
        b = Board()
        b['a1'] = Piece('K')

        for spot in ['c1', 'd1', 'e1', 'f1', 'a3', 'a4', 'a5', 'a6']:
            for piece, eval in zip(['n', 'q', 'r', 'p', 'b'], \
                                    [False, True, True, False, False]):
                b[spot] = Piece(piece)
                spot_index = coordinate_to_index(spot)
                self.assertEqual(b.piece_under_attack_straight(c2idx('a1'), b['a1'].player), eval)
                self.assertFalse(b.piece_under_attack_straight(spot_index, b[spot_index].player))
                b[spot] = None

    def test_under_attack_rook_two(self):
        b = Board()
        b['a1'] = Piece('K')
        b['a3'] = Piece('r')
        self.assertTrue(b.piece_under_attack(coordinate_to_index('a1')))

    def test_under_attack_king(self):
        b = Board()
        b['c3'] = Piece('p')

        for kingspot in ['c4', 'c2', 'b3', 'b4', 'b2', 'd3', 'd2', 'd4']:
            b[kingspot] = Piece('K')
            self.assertTrue(b.piece_under_attack(coordinate_to_index('c3')))
            b[kingspot] = None

    def test_under_attack_pawn_white_king(self):
        b = Board()
        b['c3'] = Piece('K')
        for pawn_spot, eval in zip(['b2', 'c2', 'd2', 'e2', 'b3', 'b4', 'c4', 'd4'],
                                    [False, False, False, False, False, True, False, True]):
            b[pawn_spot] = Piece('p')
            self.assertEqual(b.piece_under_attack(coordinate_to_index('c3')), eval)
            b[pawn_spot] = None
    def test_under_attack_pawn_black_king(self):
        b = Board()
        b['c3'] = Piece('k')
        for pawn_spot, eval in zip(['b2', 'c2', 'd2', 'e2', 'b3', 'b4', 'c4', 'd4'],
                                    [True, False, True, False, False, False, False, False]):
            b[pawn_spot] = Piece('P')
            index = coordinate_to_index('c3')
            self.assertEqual(b.piece_under_attack(index), eval)
            b[pawn_spot] = None

    def test_under_attack_pawn_white_king(self):
        b = Board()
        b['c3'] = Piece('K')
        b['d4'] = Piece('p')
        self.assertTrue(b.piece_under_attack(coordinate_to_index('c3')))

    def test_is_opposite_pawn(self):
        gs = Gamestate()
        b = gs.board
        self.assertTrue(is_opposite_pawn(Piece('p'), Player.WHITE))