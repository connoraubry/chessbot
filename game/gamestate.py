from game.tools import *
from game.board import Board
from game.board.piece import *
import itertools

class State():
    def __init__(self, move, castle, en_passant, halfmove_clock, fullmove_counter):
        self.move = move
        self.castle = castle
        self.en_passant = en_passant
        self.halfmove_clock = halfmove_clock
        self.fullmove_counter = fullmove_counter

class Gamestate():
    def __init__(self, FEN=starting_FEN):
        self.board = Board()
    
        self.move = Player.WHITE
        self.castle = ''
        self.en_passant = '-'
        self.halfmove_clock = 0
        self.fullmove_counter = 1

        if FEN is not None:
            self.load_FEN(FEN)
        self.get_all_moves() #set self.moves 
    
    def load_FEN(self, FEN):
        positions, move, castle, en_passant, half, full = FEN.split(" ")

        self.board.load_board_from_FEN_positions(positions)
        self.move = letter_to_player[move]
        self.castle = castle 
        self.en_passant = en_passant
        self.halfmove_clock = int(half)
        self.fullmove_counter = int(full)

    def export_FEN(self):
        positions = self.board.export_board_to_FEN_positions()

        return " ".join([positions, player_to_letter[self.move], self.castle, 
            self.en_passant, str(self.halfmove_clock),
            str(self.fullmove_counter)])

    def get_all_moves(self):
        self.moves = set()
        self.string_to_move = dict()
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

        if piece.is_pawn():
            moves = set(self.board.get_pawn_moves(index, self.move))
        elif piece.is_bishop():
            moves = set(self.board.get_bishop_moves(index, self.move))
        elif piece.is_rook():
            moves = set(self.board.get_rook_moves(index, self.move))
        elif piece.is_knight():
            moves = set(self.board.get_knight_moves(index, self.move))
        elif piece.is_king():
            moves = set(self.get_king_moves(index))
        elif piece.is_queen():
            moves = set(self.board.get_queen_moves(index, self.move))

        moves_string = {x.to_string() for x in moves}
        self.valid_moves = moves 
        self.string_to_move.update({x.to_string(): x for x in moves})
        self.move_to_start.update({move: index for move in moves_string})
        return moves_string
    

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

    def print_board(self):
        bottom = '  a b c d e f g h'
        board_2d = self.board.get_2d_representation()
        unicode_board = []
        for row in reversed(board_2d):
            unicode_row = [piece_to_unicode(x) for x in row]
            unicode_board.append(unicode_row)

        output = [bottom]
        for idx, row in enumerate(unicode_board):
            output.append("{} ".format(8-idx) + " ".join(row))
        output.append(bottom)

        for row in output:
            print(row)

    #return True if successful, false otherwise
    def take_move(self, string_move):

        if string_move in self.string_to_move:

            move = self.string_to_move[string_move]


            self.board[move.end] = self.board[move.start]
            self.board[move.start] = None


            if move.piece.is_pawn() or move.capture is not None:
                self.halfmove_clock = 0
            else:
                self.halfmove_clock += 1

            if self.move == Player.WHITE:
                self.move = Player.BLACK
            elif self.move == Player.BLACK:
                self.move = Player.WHITE

                self.fullmove_counter += 1
            
            self.get_all_moves()


    