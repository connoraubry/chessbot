from game.tools import *
import itertools
class Board():
    def __init__(self, FEN_positions=None):
        self.board = self.make_empty_board()

        #for easier checks 
        self.white_king = 'a0'
        self.black_king = 'a0'

        self.white_in_check = False 
        self.black_in_check = False 

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
                    if character == 'K':
                        self.white_king = matrix_coords_to_algebraic(real_rank, file)
                    elif character == 'k': 
                        self.black_king = matrix_coords_to_algebraic(real_rank, file)
                    file += 1
                else:
                    file += int(character)

    def get_2d_representation(self):
        return [self.board[start:start+8] for start in range(0, 64, 8)]

    def __iter__(self):
        return BoardIterator(self.board)

    def piece_under_attack(self, spot):
        player = player_of_piece(self[spot])
        return self.piece_under_attack_knight(spot, player) \
                or self.piece_under_attack_bishop(spot, player) \
                or self.piece_under_attack_rook(spot, player) \
                or self.piece_under_attack_king(spot, player) \
                or self.piece_under_attack_pawn(spot, player)

    def piece_under_attack_knight(self, spot, player=None):
        if player == None:
            player = player_of_piece(self[spot])

        index = coordinate_to_index(spot)

        file_idx = file_to_idx[spot[0]]
        rank_idx = int(spot[1]) - 1
        move_offsets = []

        if rank_idx >= 1:
            if file_idx >= 2:
                move_offsets.append(-10)
            if file_idx <= 5:
                move_offsets.append(-6)
            if rank_idx >= 2:
                if file_idx >= 1:
                    move_offsets.append(-17)
                if file_idx <= 6:
                    move_offsets.append(-15) 
        if rank_idx <= 6:
            if file_idx >= 2:
                move_offsets.append(6)
            if file_idx <= 5:
                move_offsets.append(10)
            if rank_idx <= 5:
                if file_idx >= 1:
                    move_offsets.append(15)
                if file_idx <= 6:
                    move_offsets.append(17) 

        for move_offset in move_offsets:
            new_index = index + move_offset
            piece = self.board[new_index]
            if is_opposite_knight(piece, player):
                return True
        return False

    def piece_under_attack_bishop(self, spot, player=None):
        if player == None:
            player = player_of_piece(self[spot])

        index = coordinate_to_index(spot)
        file_idx = file_to_idx[spot[0]]
        rank_idx = int(spot[1]) - 1

        for file_diff, rank_diff in [[1, 1], [-1, 1], [-1, -1], [1, -1]]:
            curr_file_idx = file_idx + file_diff
            curr_rank_idx = rank_idx + rank_diff
            while ( 0 <= curr_file_idx < 8 and 0 <= curr_rank_idx < 8):
                new_spot = curr_file_idx + (curr_rank_idx * 8)
                piece  = self.board[new_spot]
                if piece is None:
                    curr_file_idx += file_diff
                    curr_rank_idx += rank_diff
                elif is_opposite_queen_or_bishop(piece, player):
                        return True
                else:
                    break

        return False

    def piece_under_attack_rook(self, spot, player=None):
        if player == None:
            player = player_of_piece(self[spot])

        file_idx = file_to_idx[spot[0]]
        rank_idx = int(spot[1]) - 1

        for file_diff in [1, -1]:
            curr_file_idx = file_idx + file_diff
            while (0 <= curr_file_idx < 8):
                new_spot = curr_file_idx + (rank_idx * 8)
                piece  = self.board[new_spot]
                if piece == None:
                    curr_file_idx += file_diff
                elif is_opposite_queen_or_rook(piece, player):
                    return True
                else:
                    break  

        for rank_diff in [1, -1]:
            curr_rank_idx = rank_idx + rank_diff
            while (0 <= curr_rank_idx < 8):
                new_spot = file_idx + (curr_rank_idx * 8)
                piece  = self.board[new_spot]
                if piece == None:
                    curr_rank_idx += rank_diff
                elif is_opposite_queen_or_rook(piece, player):
                    return True 
                else:
                    break
        return False

    def piece_under_attack_king(self, spot, player=None):
        if player == None:
            player = player_of_piece(self[spot])

        file_idx = file_to_idx[spot[0]]
        rank_idx = int(spot[1]) - 1

        for rank_diff, file_diff in itertools.product([-1, 0, 1], [-1, 0, 1]): 
            curr_file_idx = file_idx + file_diff
            curr_rank_idx = rank_idx + rank_diff
            if ( 0 <= curr_file_idx < 8 and 0 <= curr_rank_idx < 8):
                new_spot = curr_file_idx + (curr_rank_idx * 8)
                piece  = self.board[new_spot]
                
                if is_opposite_king(piece, player):
                    return True
        return False 

    def piece_under_attack_pawn(self, spot, player=None):
        if player == None:
            player = player_of_piece(self[spot])

        file_idx = file_to_idx[spot[0]]
        rank_idx = int(spot[1]) - 1

        if player == 'w':
            rank_diff = 1
        elif player == 'b':
            rank_diff = -1
        for file_diff in [-1, 1]:
            curr_file_idx = file_idx + file_diff
            curr_rank_idx = rank_idx + rank_diff

            if ( 0 <= curr_file_idx < 8 and 0 <= curr_rank_idx < 8):
                new_spot = curr_file_idx + (curr_rank_idx * 8)
                piece  = self.board[new_spot]

                if is_opposite_pawn(piece, player):
                    return True
        return False 

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

def is_opposite_knight(piece, player):
    if player == 'w':
        return piece == 'n'
    if player == 'b':
        return piece == 'N'
    return False

def is_opposite_bishop(piece, player):
    if player == 'w':
        return piece == 'b'
    if player == 'b':
        return piece == 'B'
    return False 
def is_opposite_queen(piece, player):
    if player == 'w':
        return piece == 'q'
    if player == 'b':
        return piece == 'Q'
    return False 
def is_opposite_rook(piece, player):
    if player == 'w':
        return piece == 'r'
    if player == 'b':
        return piece == 'R'
    return False 

def is_opposite_king(piece, player):
    if player == 'w':
        return piece == 'k'
    if player == 'b':
        return piece == 'K'
    return False 
def is_opposite_pawn(piece, player):
    if player == 'w':
        return piece == 'p'
    if player == 'b':
        return piece == 'P'
    return False 
def is_opposite_queen_or_bishop(piece, player):
    return is_opposite_bishop(piece, player) or is_opposite_queen(piece, player)

def is_opposite_queen_or_rook(piece, player):
    return is_opposite_rook(piece, player) or is_opposite_queen(piece, player)