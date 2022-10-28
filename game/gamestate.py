from game.tools import *
from game.board import Board
from game.board.piece import *
import itertools
from collections import defaultdict
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
    
    #Load gametstate from FEN 
    def load_FEN(self, FEN):
        positions, move, castle, en_passant, half, full = FEN.split(" ")

        self.board.load_board_from_FEN_positions(positions)
        self.move = letter_to_player[move]
        self.castle = castle 
        self.en_passant = c2idx(en_passant)
        self.halfmove_clock = int(half)
        self.fullmove_counter = int(full)

    #export gamestate to FEN
    def export_FEN(self):
        positions = self.board.export_board_to_FEN_positions()

        return " ".join([positions, player_to_letter[self.move], self.castle, 
            index_to_coordinate(self.en_passant), str(self.halfmove_clock),
            str(self.fullmove_counter)])

    #get all valid moves for the current player 
    def get_all_moves(self, checkmate_check=False):
        self.string_to_move = dict()
        moves = set()

        attack_spot_to_source_spots = defaultdict(lambda: defaultdict(set))

        for idx, piece in enumerate(self.board):
            if player_of_piece(piece) == self.move:
                valid_moves, attack_spots = self.get_move(idx, checkmate_check=checkmate_check)
                moves.update(valid_moves)

                for attack in attack_spots.keys():
                    for piece in attack_spots[attack].keys():
                        attack_spot_to_source_spots[attack][piece].update(attack_spots[attack][piece])

        self.attack_spot_to_source_spots = attack_spot_to_source_spots
        self.string_to_move = {x.to_string(): x for x in moves}
        return set(self.string_to_move.keys())

    def attack_spot_function(self, attack_spot, piece):
        return self.attack_spot_to_source_spots[attack_spot][piece]

    #Get all valid moves for a board index. 
    def get_move(self, index, checkmate_check=False):
        moves = set()
        attack_spot_to_source_spots = defaultdict(lambda: defaultdict(set))
        piece = self.board[index]
        if type(index) == str:
            index = coordinate_to_index(index)

        if piece is None:
            return set(), set()
        # if checkmate_check:
        #     print(piece)
        if piece.is_pawn():
            moves = set(self.board.get_pawn_moves(index, en_passant=self.en_passant))
        elif piece.is_bishop():
            moves = set(self.board.get_bishop_moves(index))
        elif piece.is_rook():
            moves = set(self.board.get_rook_moves(index))
        elif piece.is_knight():
            moves = set(self.board.get_knight_moves(index))
        elif piece.is_king():
            moves = set(self.get_king_moves(index))
        elif piece.is_queen():
            moves = set(self.board.get_queen_moves(index))

        valid_moves = set()
        for m in moves:
            self.temp_move(m)
            king_check = self.board.king_in_check()


            #opponent king in check, see if it's mate.
            #not checkmate_check skips this if we're a level deep
            if not checkmate_check and king_check[opponent[self.move]]:
                # self.print_board()
                # print(self.board.board)
                m.check = True 
                self.move = opponent[self.move]
                if m.check and len(self.get_all_moves(checkmate_check=True)) == 0:
                    m.checkmate = True 
                self.move = opponent[self.move]


            if not king_check[self.move]:
                attack_spot_to_source_spots[m.end][m.piece.piece].add(m.start)
                m.attack_spot_function = self.attack_spot_function
                valid_moves.add(m)

            self.reverse_temp_move(m)

        return valid_moves, attack_spot_to_source_spots
    
    #TODO: Castling
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

        return moves 

    #Print the board all nice 
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
        print("Taking", string_move)
        if string_move in self.string_to_move:

            move = self.string_to_move[string_move]

            self.board[move.end] = self.board[move.start]
            self.board[move.start] = None

            if move.en_passant_piece_spot is not None:
                self.board[move.en_passant_piece_spot] = None

            if move.promotion is not None:
                self.board[move.end] = move.promotion


            if move.en_passant_revealed_spot is not None:
                self.en_passant = move.en_passant_revealed_spot
            else:
                self.en_passant = -1

            if move.piece.is_king():
                if move.piece.is_white():
                    self.board.white_king = move.end 
                elif move.piece.is_black():
                    self.board.black_king = move.end 

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
    
    #Take a move that does not update state. Can be reversed 
    def temp_move(self, move):
        self.board[move.end] =  move.piece 
        self.board[move.start] = None

        if move.en_passant_piece_spot is not None:
            self.board[move.en_passant_piece_spot] = None

        if move.promotion is not None:
            self.board[move.end] = move.promotion

        if move.piece.is_king():
            if move.piece.is_white():
                self.board.white_king = move.end 
            elif move.piece.is_black():
                self.board.black_king = move.end 

    def reverse_temp_move(self, move):
        self.board[move.start] =  move.piece 
        self.board[move.end] = move.capture 

        if move.en_passant_piece_spot is not None:
            self.board[move.en_passant_piece_spot] = move.capture 
            self.board[move.end] = None

        if move.piece.is_king():
            if move.piece.is_white():
                self.board.white_king = move.start 
            elif move.piece.is_black():
                self.board.black_king = move.start 

    def get_score(self):
        score = 0
        peice_to_score = {
            PieceName.KING: 10000,
            PieceName.QUEEN: 900,
            PieceName.ROOK: 500,
            PieceName.BISHOP: 300,
            PieceName.KNIGHT: 300,
            PieceName.PAWN: 100,
        }
        operator = {
            Player.WHITE: 1,
            Player.BLACK: -1       
        }

        for piece in self.board:
            if piece is not None:
                score += operator[piece.player] * peice_to_score[piece.piece]
        return score 