from operator import index
import unittest
import itertools

from game.tools import *

class HelperTester(unittest.TestCase):

    def test_valid_coordinates(self):

        for r in itertools.product(valid_files, valid_ranks): 
            coordinate = r[0] + r[1]
            self.assertTrue(is_coordinate_valid(coordinate))

        self.assertFalse(is_coordinate_valid(23))
        invalid_files = [l for l in "ijklmnopqrstuvwxyzABCDEFGHI"]
        invalid_ranks = ['9', '0', '-1', '10']
        for r in itertools.product(invalid_files, invalid_ranks): 
            coordinate = r[0] + r[1]
            self.assertFalse(is_coordinate_valid(coordinate))

    def test_index_to_coordinate(self):
        for idx, r in enumerate(itertools.product(valid_ranks, valid_files)): 
            coordinate = r[1] + r[0]
            self.assertEqual(coordinate, index_to_coordinate(idx))
    def test_coordinate_to_index(self):
        for idx, r in enumerate(itertools.product(valid_ranks, valid_files)): 
            coordinate = r[1] + r[0]
            self.assertEqual(idx, coordinate_to_index(coordinate))
    def test_piece_player(self):
        for piece in 'prnbqk':
            self.assertEqual('b', player_of_piece(piece))
        for piece in 'PRNBQK':
            self.assertEqual('w', player_of_piece(piece))