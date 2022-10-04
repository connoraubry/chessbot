from shutil import move
from game.tools import *
from game.board import Board 
import itertools

class Gamestate():
    def __init__(self, fen=starting_FEN):
        self.board = Board()
        self.load_FEN(fen)
    
    def load_FEN(self, FEN):
        if FEN is not None:
            positions, move, castle, en_passant, half, full = FEN.split(" ")

            self.board.load_board_from_FEN_positions(positions)
            self.move = move 
            self.castle = castle 
            self.en_passant = en_passant
            self.halfmove_clock = int(half)
            self.fullmove_counter = int(full)
        else:
            self.move = 'w'
            self.castle = ''
            self.en_passant = '-'
            self.halfmove_clock = 0
            self.fullmove_counter = 1
    
    def get_all_moves(self):
        moves = set()
        for idx, piece in enumerate(self.board):
            if player_of_piece(piece) == self.move:
                moves.update(self.get_move(idx)) 
        return moves

    def get_move(self, index):
        piece = self.board[index]
        if type(index) == str:
            index = coordinate_to_index(index)

        if piece is None:
            return set()

        piece = piece.lower()
        if piece == 'p':
            return set(self.get_pawn_moves(index))
        elif piece == 'b':
            return {"B" + x for x in self.get_bishop_moves(index)}
        elif piece == 'r':
            return {"R" + x for x in self.get_rook_moves(index)}
        elif piece == 'n':
            return {"N" + x for x in self.get_knight_moves(index)}
        elif piece == 'k':
            return {"K" + x for x in self.get_king_moves(index)}
        elif piece == 'q':
            return {"Q" + x for x in self.get_queen_moves(index)}
        return set()

    #TODO: promotion, capture, side of board captures
    def get_pawn_moves(self, index):
        algebraic = index_to_coordinate(index)
        #check move ahead
        moves = []

        if self.board[index+8] is None:
            moves.append(index_to_coordinate(index+8))
            #if space ahead is empty, and first rank can go 2 moves
            if (algebraic[1] == '2' and self.move == 'w') or \
            (algebraic[1] == '7' and self.move == 'b'):
                if self.board[index+16] is None:
                    moves.append(index_to_coordinate(index+16))

        return moves

    def get_knight_moves(self, index):
        moves = []

        algebraic = index_to_coordinate(index)
        file_idx = file_to_idx[algebraic[0]]
        rank_idx = int(algebraic[1]) - 1
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
            if self.board[new_index] == None:
                moves.append(index_to_coordinate(index + move_offset))
            elif player_of_piece(self.board[new_index]) != self.move:
                moves.append("x" + index_to_coordinate(index + move_offset))
        return moves

    def get_bishop_moves(self, index):
        algebraic = index_to_coordinate(index)
        file_idx = file_to_idx[algebraic[0]]
        rank_idx = int(algebraic[1]) - 1
        moves = []

        for file_diff, rank_diff in [[1, 1], [-1, 1], [-1, -1], [1, -1]]:
            curr_file_idx = file_idx + file_diff
            curr_rank_idx = rank_idx + rank_diff
            while ( 0 <= curr_file_idx < 8 and 0 <= curr_rank_idx < 8):
                new_spot = curr_file_idx + (curr_rank_idx * 8)
                board_piece  = self.board[new_spot]
                if board_piece == None:
                    moves.append(index_to_coordinate(new_spot))
                    curr_file_idx += file_diff
                    curr_rank_idx += rank_diff
                elif player_of_piece(board_piece) != self.move:
                    moves.append("x" + index_to_coordinate(new_spot))
                    break 
                else:
                    break
        return moves

    def get_rook_moves(self, index):
        algebraic = index_to_coordinate(index)
        file_idx = file_to_idx[algebraic[0]]
        rank_idx = int(algebraic[1]) - 1
        moves = []

        for file_diff in [1, -1]:
            curr_file_idx = file_idx + file_diff
            while (0 <= curr_file_idx < 8):
                new_spot = curr_file_idx + (rank_idx * 8)
                board_piece  = self.board[new_spot]
                if board_piece == None:
                    moves.append(index_to_coordinate(new_spot))
                elif player_of_piece(board_piece) != self.move:
                    moves.append("x" + index_to_coordinate(new_spot))
                    break 
                else:
                    break        
                curr_file_idx += file_diff
        for rank_diff in [1, -1]:
            curr_rank_idx = rank_idx + rank_diff
            while (0 <= curr_rank_idx < 8):
                new_spot = file_idx + (curr_rank_idx * 8)
                board_piece  = self.board[new_spot]
                if board_piece == None:
                    moves.append(index_to_coordinate(new_spot))
                elif player_of_piece(board_piece) != self.move:
                    moves.append("x" + index_to_coordinate(new_spot))
                    break 
                else:
                    break        
                curr_rank_idx += rank_diff
        return moves

    def get_king_moves(self, index):
        algebraic = index_to_coordinate(index)
        file_idx = file_to_idx[algebraic[0]]
        rank_idx = int(algebraic[1]) - 1
        moves = []
        for rank_diff, file_diff in itertools.product([-1, 0, 1], [-1, 0, 1]): 
            curr_file_idx = file_idx + file_diff
            curr_rank_idx = rank_idx + rank_diff
            if ( 0 <= curr_file_idx < 8 and 0 <= curr_rank_idx < 8):
                new_spot = curr_file_idx + (curr_rank_idx * 8)
                board_piece  = self.board[new_spot]
                if board_piece == None:
                    moves.append(index_to_coordinate(new_spot))
                elif player_of_piece(board_piece) != self.move:
                    moves.append("x" + index_to_coordinate(new_spot))
        return moves 

    def get_queen_moves(self, index):
        bishop = self.get_bishop_moves(index)
        rook = self.get_rook_moves(index)
        return bishop + rook

    def print_board(self):
        bottom = '  a b c d e f g h'
        board_2d = self.board.get_2d_representation()
        unicode_board = []
        for row in reversed(board_2d):
            unicode_row = [piece_to_unicode[x] for x in row]
            unicode_board.append(unicode_row)

        output = [bottom]
        for idx, row in enumerate(unicode_board):
            output.append("{} ".format(8-idx) + " ".join(row))
        output.append(bottom)

        for row in output:
            print(row)

        