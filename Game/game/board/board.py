from game.tools import *

class Board():
    def __init__(self, FEN_positions=None):
        self.board = self.make_empty_board()
        if FEN_positions is not None:
            self.load_board_from_FEN_positions(FEN_positions)

    def make_empty_board(self):
        return [None for x in range(64)]

    def __getitem__(self, key):
        if type(key) == int:
            return self.board[key]
        if not is_coordinate_valid(key):
            raise ValueError("{} is not a valid coordinate".format(key))
        file_idx = file_to_idx[key[0]]
        rank_idx = rank_to_idx[key[1]]
        return self.board[file_idx + (rank_idx * 8)]

    def __setitem__(self, key, value):
        if type(key) == int:
            self.board[key] = value
        if not is_coordinate_valid(key):
            raise ValueError("{} is not a valid coordinate".format(key))
        file_idx = file_to_idx[key[0]]
        rank_idx = rank_to_idx[key[1]]
        self.board[file_idx + (rank_idx * 8)] = value 

    def load_board_from_FEN_positions(self, positions):
        for inverted_idx, rank in enumerate(positions.split("/")):
            real_rank = 7-inverted_idx
            file = 0
            for character in rank:

                if character in valid_pieces:
                    self.board[file + (real_rank * 8)] = character
                    file += 1
                else:
                    file += int(character)

    def get_2d_representation(self):
        return [self.board[start:start+8] for start in range(0, 64, 8)]

    def __iter__(self):
        return BoardIterator(self.board)

class BoardIterator():
    def __init__(self, board):
        self.board = board
        self._idx = 0
    def __next__(self):
        if self._idx < len(self.board):
            result = self.board[self._idx]
            self._idx += 1
            return result 
        raise StopIteration


def matrix_coords_to_algebraic(rank, file):
    return idx_to_file[file] + idx_to_rank[rank]
