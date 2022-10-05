from game.tools import *
from game.board import Board 
import itertools

class Gamestate():
    def __init__(self, fen=starting_FEN):
        self.board = Board()
        self.load_FEN(fen)
        self.get_all_moves() #set self.moves 
    
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
        self.moves = set()
        self.move_to_start = dict()
        for idx, piece in enumerate(self.board):
            if player_of_piece(piece) == self.move:
                self.moves.update(self.get_move(idx)) 

        return self.moves

    def get_move(self, index):
        moves = set()

        piece = self.board[index]
        if type(index) == str:
            index = coordinate_to_index(index)

        if piece is None:
            return set()

        piece = piece.upper()
        if piece == 'P':
            moves = set(self.get_pawn_moves(index))
        elif piece == 'B':
            moves = set(self.get_bishop_moves(index))
        elif piece == 'R':
            moves = set(self.get_rook_moves(index))
        elif piece == 'N':
            moves = set(self.get_knight_moves(index))
        elif piece == 'K':
            moves = set(self.get_king_moves(index))
        elif piece == 'Q':
            moves = set(self.get_queen_moves(index))

        if piece != 'P':
            moves =  {piece + x for x in moves }

        self.move_to_start.update({move: index for move in moves})
        return moves

    #TODO: promotion, capture, side of board captures
    def get_pawn_moves(self, index):
        algebraic = index_to_coordinate(index)
        #check move ahead
        moves = []

        offset = 0
        if self.move == 'w':
            offset = 8
        elif self.move == 'b':
            offset = -8

        if self.board[index + offset] is None:
            moves.append(index_to_coordinate(index+offset))
            #if space ahead is empty, and first rank can go 2 moves
            if (algebraic[1] == '2' and self.move == 'w') or \
            (algebraic[1] == '7' and self.move == 'b'):
                if self.board[index+ (offset * 2)] is None:
                    moves.append(index_to_coordinate(index + (offset * 2)))

        for attack_space in [offset + 1, offset - 1]:
            piece = self.board[attack_space]
            if piece is not None and player_of_piece(piece) != self.move:
                moves.append(algebraic[0] + 'x' + index_to_coordinate(attack_space))
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
        # for castle_option in self.get_valid_castling():
        #     if castle_option.lower() == 'k':
        #         if self.board[index + 1] == self.board[index + 2] == None:

        return moves 

    def get_valid_castling(self):
        valid = []
        for letter in self.castle:
            if self.move == 'w':
                if letter == letter.upper():
                    valid.append(letter)
            if self.move == 'b':
                if letter == letter.lower():
                    valid.append(letter)
        return valid 

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

    #return True if successful, false otherwise
    def take_move(self, move):
        print(move)
        if move in self.moves:

            destination_spot = move[-2:]
            print(destination_spot)

            source_spot = self.move_to_start[move]
            self.board[destination_spot] = self.board[source_spot]
            self.board[source_spot] = None


            self.move = 'w' if self.move == 'b' else 'b' 