import unittest
from game import * 
from tests.constants import *

def load_file(filepath):
    with open(filepath, 'r') as fp:
        lines = fp.readlines()
    fen = lines[0]
    valid_moves = set([x.strip('\n') for x in lines[1:]])
    return fen, valid_moves

class MoveTester(unittest.TestCase):

    def test_testone(self):
        self.filetester('testone.txt')
    def test_testtwo(self):
        self.filetester('testtwo.txt')
    def test_testthree(self):
        self.filetester('testthree.txt')
    def test_testfour(self):
        self.filetester('testfour.txt')
    def test_testfive(self):
        self.filetester('testfive.txt')
    def test_testsix(self):
        self.filetester('testsix.txt')

    def filetester(self, name):
        fen, valid_moves = load_file(fen_plus_moves_path / name)
        g = Gamestate(FEN=fen)
        self.assertSetEqual(valid_moves, g.get_all_moves())