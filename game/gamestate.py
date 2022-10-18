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
    def export_FEN(self):
        positions = self.board.export_board_to_FEN_positions()

        return " ".join([positions, self.move, self.castle, 
            self.en_passant, str(self.halfmove_clock),
            str(self.fullmove_counter)])

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

        # if piece != 'P':
        #     moves =  {piece + x for x in moves }
        moves = {x.to_string() for x in moves}
        self.move_to_start.update({move: index for move in moves})
        return moves

    #TODO: promotion, capture, side of board captures
    def get_pawn_moves(self, index):
        rank, _ = rank_and_file(index)
        #check move ahead
        moves = []

        offset = 0
        if self.move == 'w':
            offset = 8
        elif self.move == 'b':
            offset = -8
        new_spot = index + offset
        if self.board[new_spot] is None:
            moves.append(Move(index, new_spot, self.board[index], None))
            #if space ahead is empty, and first rank can go 2 moves
            if (rank == 1 and self.move == 'w') or \
            (rank == 6 and self.move == 'b'):
                two_spot = new_spot + offset 
                if self.board[two_spot] is None:
                    moves.append(Move(index, two_spot, self.board[index], None))

        for attack_offset in [offset + 1, offset - 1]:
            attack_spot = index + attack_offset
            piece = self.board[attack_spot]
            if piece is not None and player_of_piece(piece) != self.move:
                moves.append(Move(index, new_spot, self.board[index], piece))
        return moves

    def get_knight_moves(self, index):

        rank, file = rank_and_file(index)

        move_offsets = []
        moves = []


        if rank >= 1:
            if file >= 2:
                move_offsets.append(-10)
            if file <= 5:
                move_offsets.append(-6)
            if rank >= 2:
                if file >= 1:
                    move_offsets.append(-17)
                if file <= 6:
                    move_offsets.append(-15)  
        if rank <= 6:
            if file >= 2:
                move_offsets.append(6)
            if file <= 5:
                move_offsets.append(10)
            if rank <= 5:
                if file >= 1:
                    move_offsets.append(15)
                if file <= 6:
                    move_offsets.append(17) 

        for move_offset in move_offsets:
            new_index = index + move_offset
            if player_of_piece(self.board[new_index]) != self.move:
                moves.append(Move(index, new_index, self.board[index], self.board[new_index]))
        return moves

    def get_bishop_moves(self, index):
        rank, file = rank_and_file(index)

        moves = []

        for file_diff, rank_diff in [[1, 1], [-1, 1], [-1, -1], [1, -1]]:
            curr_file_idx = file + file_diff
            curr_rank_idx = rank + rank_diff
            while ( 0 <= curr_file_idx < 8 and 0 <= curr_rank_idx < 8):
                new_spot = curr_file_idx + (curr_rank_idx * 8)
                board_piece  = self.board[new_spot]
                if board_piece == None:
                    moves.append(Move(index, new_spot, self.board[index], board_piece))
                    curr_file_idx += file_diff
                    curr_rank_idx += rank_diff
                elif player_of_piece(board_piece) != self.move:
                    moves.append(Move(index, new_spot, self.board[index], board_piece))
                    break 
                else:
                    break
        return moves

    def get_rook_moves(self, index):
        rank, file = rank_and_file(index)
        moves = []

        for file_diff in [1, -1]:
            curr_file_idx = file + file_diff
            while (0 <= curr_file_idx < 8):
                new_spot = curr_file_idx + (rank * 8)
                board_piece  = self.board[new_spot]
                if board_piece == None:
                    moves.append(Move(index, new_spot, self.board[index], board_piece))
                elif player_of_piece(board_piece) != self.move:
                    moves.append(Move(index, new_spot, self.board[index], board_piece))
                    break 
                else:
                    break        
                curr_file_idx += file_diff
        for rank_diff in [1, -1]:
            curr_rank_idx = rank + rank_diff
            while (0 <= curr_rank_idx < 8):
                new_spot = file + (curr_rank_idx * 8)
                board_piece  = self.board[new_spot]
                if board_piece == None:
                    moves.append(Move(index, new_spot, self.board[index], board_piece))
                elif player_of_piece(board_piece) != self.move:
                    moves.append(Move(index, new_spot, self.board[index], board_piece))
                    break 
                else:
                    break        
                curr_rank_idx += rank_diff
        return moves

    def get_king_moves(self, index):
        rank, file = rank_and_file(index)

        moves = []
        for rank_diff, file_diff in itertools.product([-1, 0, 1], [-1, 0, 1]): 
            curr_file_idx = file + file_diff
            curr_rank_idx = rank + rank_diff
            if ( 0 <= curr_file_idx < 8 and 0 <= curr_rank_idx < 8):
                new_spot = curr_file_idx + (curr_rank_idx * 8)
                board_piece  = self.board[new_spot]
                if board_piece == None:
                    moves.append(Move(index, new_spot, self.board[index], board_piece))
                elif player_of_piece(board_piece) != self.move:
                    moves.append(Move(index, new_spot, self.board[index], board_piece))
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

            if self.board[destination_spot] in ['p', 'P']:
                self.halfmove_clock = 0
            elif 'x' in move:
                self.halfmove_clock = 0
            else:
                self.halfmove_clock += 1

            if self.move == 'w':
                self.move = 'b'
            elif self.move == 'b':
                self.move = 'w'

                self.fullmove_counter += 1