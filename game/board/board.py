from game.tools import *
from game.board.piece import Piece, get_opposite_piece
import itertools

class Board():
    def __init__(self, FEN_positions=None):
        self.board = self.make_empty_board()

        #for easier checks 
        self.white_king = -1
        self.black_king = -1

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
        if type(value) == int:
            print("setting {} to {}".format(key, value))
        if type(key) == int:
            self.board[key] = value
            return
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
                    index  = file + (real_rank * 8)
                    self.board[index] = Piece(character)
                    if character == 'K':
                        self.white_king = index
                    elif character == 'k': 
                        self.black_king = index
                    file += 1
                else:
                    file += int(character)

    def export_board_to_FEN_positions(self):
        board_2d = self.get_2d_representation()
        fen_rows = []
        
        for row in reversed(board_2d):
            fen_row = ""
            file_idx = 0
            while file_idx < 8:
                piece = row[file_idx]
                if piece is not None:
                    fen_row += piece.to_string()
                    file_idx += 1
                else:
                    space_counter = 0
                    while (file_idx < 8 and row[file_idx] is None):
                        file_idx += 1
                        space_counter += 1
                    fen_row += str(space_counter)
            fen_rows.append(fen_row)

        return "/".join(fen_rows)

    def get_2d_representation(self):
        return [self.board[start:start+8] for start in range(0, 64, 8)]

    def __iter__(self):
        return BoardIterator(self.board)

    def king_in_check(self):
        white_check = False 
        black_check = False 

        if self.white_king != -1:
            white_check = self.piece_under_attack(self.white_king)
        if self.black_king != -1:
            black_check = self.piece_under_attack(self.black_king)
        return {
            Player.WHITE: white_check,
            Player.BLACK: black_check
        }

    def piece_under_attack(self, spot):
        player = self[spot].player
        return self.piece_under_attack_by_knight(spot, player) \
                or self.piece_under_attack_diagonal(spot, player) \
                or self.piece_under_attack_straight(spot, player) \
                or self.piece_under_attack_by_king(spot, player) \
                or self.piece_under_attack_by_pawn(spot, player)

    def piece_under_attack_by_knight(self, spot, player):
        if player == None:
            player = self[spot].player
        knight_moves = self.get_knight_moves(spot, player)
        for km in knight_moves:
            if km.capture == get_opposite_piece(player, 'knight'):
                return True 
        return False

    def piece_under_attack_diagonal(self, index, player):
        if player == None:
            player = self[index].player
        bishop_moves = self.get_bishop_moves(index, player)
        for move in bishop_moves:
            if move.capture == get_opposite_piece(player, 'bishop') or \
                move.capture == get_opposite_piece(player, 'queen'):
                return True
        return False
    
    def piece_under_attack_straight(self, index, player):
        if player == None:
            player = self[index].player
        rook_moves = self.get_rook_moves(index, player)
        for move in rook_moves:
            if move.capture == get_opposite_piece(player, 'rook') or \
                move.capture == get_opposite_piece(player, 'queen'):
                return True 
        return False 

    def piece_under_attack_by_king(self, index, player):
        if player == None:
            player = self[index].player

        rank_idx, file_idx = rank_and_file(index)

        for rank_diff, file_diff in itertools.product([-1, 0, 1], [-1, 0, 1]): 
            curr_file_idx = file_idx + file_diff
            curr_rank_idx = rank_idx + rank_diff
            if ( 0 <= curr_file_idx < 8 and 0 <= curr_rank_idx < 8):
                new_spot = curr_file_idx + (curr_rank_idx * 8)
                piece  = self.board[new_spot]
                
                if is_opposite_king(piece, player):
                    return True
        return False 

    def get_knight_moves(self, index, player=None):
        if player == None:
            player = self[index].player
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
            # print(new_index)
            # print(self[new_index])

            if player_of_piece(self[new_index]) != player:
                moves.append(Move(index, new_index, self[index], self[new_index]))
        return moves

    def get_bishop_moves(self, index, player=None):
        if player == None:
            player = self[index].player
        rank, file = rank_and_file(index)

        moves = []

        for file_diff, rank_diff in [[1, 1], [-1, 1], [-1, -1], [1, -1]]:
            curr_file_idx = file + file_diff
            curr_rank_idx = rank + rank_diff
            while ( 0 <= curr_file_idx < 8 and 0 <= curr_rank_idx < 8):
                new_spot = curr_file_idx + (curr_rank_idx * 8)
                board_piece  = self[new_spot]
                if board_piece == None:
                    moves.append(Move(index, new_spot, self[index], board_piece))
                    curr_file_idx += file_diff
                    curr_rank_idx += rank_diff
                elif player_of_piece(board_piece) != player:
                    moves.append(Move(index, new_spot, self[index], board_piece))
                    break 
                else:
                    break
        return moves

    def get_rook_moves(self, index, player=None):
        if player == None:
            player = self[index].player
        rank, file = rank_and_file(index)
        moves = []

        for file_diff in [1, -1]:
            curr_file_idx = file + file_diff
            while (0 <= curr_file_idx < 8):
                new_spot = curr_file_idx + (rank * 8)
                board_piece  = self[new_spot]
                if board_piece == None:
                    moves.append(Move(index, new_spot, self[index], board_piece))
                elif player_of_piece(board_piece) != player:
                    moves.append(Move(index, new_spot, self[index], board_piece))
                    break 
                else:
                    break        
                curr_file_idx += file_diff
        for rank_diff in [1, -1]:
            curr_rank_idx = rank + rank_diff
            while (0 <= curr_rank_idx < 8):
                new_spot = file + (curr_rank_idx * 8)
                board_piece  = self[new_spot]
                if board_piece == None:
                    moves.append(Move(index, new_spot, self[index], board_piece))
                elif player_of_piece(board_piece) != player:
                    moves.append(Move(index, new_spot, self[index], board_piece))
                    break 
                else:
                    break        
                curr_rank_idx += rank_diff
        return moves

    def get_queen_moves(self, index, player=None):
        bishop = self.get_bishop_moves(index, player)
        rook = self.get_rook_moves(index, player)
        return bishop + rook

    #TODO: Castling
    def get_king_moves(self, index, player=None, castling=''):
        if player == None:
            player = self[index].player
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
                elif player_of_piece(board_piece) != player:
                    moves.append(Move(index, new_spot, self.board[index], board_piece))
        moves += self.get_valid_castles(index, castling)
        return moves 

    def get_valid_castles(self, index, castling=''):
        piece = self.board[index]
        moves = set()
        if piece is not None:
            if piece.player == Player.WHITE:
                if 'K' in castling:
                    if self.board[5] == self.board[6] == None:
                        moves.add(Move(index, 6, piece, None, castle='K'))
                if 'Q' in castling:
                    if self.board[3] == self.board[2] == self.board[1] == None:
                        moves.add(Move(index, 2, piece, None, castle='Q'))
            elif piece.player == Player.BLACK:
                if 'k' in castling:
                    if self.board[61] == self.board[62] == None:
                        moves.add(Move(index, 62, piece, None, castle='k'))
                if 'q' in castling:
                    if self.board[59] == self.board[58] == self.board[57] == None:
                        moves.add(Move(index, 58, piece, None, castle='q'))
        return moves 

    #TODO: promotion, capture, side of board captures
    def get_pawn_moves(self, index, player=None, en_passant=None):
        if player == None:
            player = self[index].player
        rank, file = rank_and_file(index)
        #check move ahead
        moves = []

        if rank == 0 or rank == 7:
            return []

        offset = 0
        if player == Player.WHITE:
            offset = 8
        elif player == Player.BLACK:
            offset = -8
        one_spot = index + offset

        one_spot_piece = self.board[one_spot]
        if one_spot_piece is None:

            #promotions
            if (rank == 6 and player == Player.WHITE) or \
               (rank == 1 and player == Player.BLACK):
                pass
                for promote in promotion_pieces:
                    promotion_piece = Piece(pieceName=promote, player=self.board[index].player)
                    moves.append(Move(index, one_spot, 
                                self.board[index], one_spot_piece, 
                                promotion=promotion_piece))
            #no promotion, just regular move up
            else:
                moves.append(Move(index, one_spot, self.board[index], one_spot_piece))


            #if space ahead is empty, and first rank can go 2 moves
            if (rank == 1 and player == Player.WHITE) or \
            (rank == 6 and player == Player.BLACK):
                two_spot = one_spot + offset 
                if self.board[two_spot] is None:
                    moves.append(Move(index, two_spot, 
                            self.board[index], None, en_passant_revealed_spot=one_spot))

        #can't capture off side of board 
        attack_offsets = []
        if file != 0:
            attack_offsets.append(offset-1)
        if file != 7:
            attack_offsets.append(offset+1)

        for attack_offset in attack_offsets:
            attack_spot = index + attack_offset
            attack_piece = self.board[attack_spot]
            if type(attack_piece) == int:
                print(attack_piece)
                print(self.board)
            if attack_piece is not None and player_of_piece(attack_piece) != player:
                #promotion attack
                if (rank == 6 and player == Player.WHITE) or \
                    (rank == 1 and player == Player.BLACK):
                    pass
                    for promote in promotion_pieces:
                        promotion_piece = Piece(pieceName=promote, player=self.board[index].player)
                        moves.append(Move(index, attack_spot, 
                                    self.board[index], attack_piece, promotion=promotion_piece))
                #normal attack 
                else:
                    moves.append(Move(index, attack_spot, self.board[index], attack_piece))
            #en passant 
            elif en_passant == attack_spot:
                en_passant_piece_spot = -1
                if en_passant < 32:
                    en_passant_piece_spot = en_passant + 8
                else:
                    en_passant_piece_spot = en_passant - 8
                
                moves.append(Move(index, attack_spot, self.board[index], self.board[en_passant_piece_spot],
                             en_passant_piece_spot=en_passant_piece_spot))
        return moves

    def piece_under_attack_by_pawn(self, index, player):
        if player == None:
            player = self[index].player

        rank_idx, file_idx = rank_and_file(index)

        if player == Player.WHITE:
            rank_diff = 1
        elif player == Player.BLACK:
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
    return piece == Piece(opposite_piece[player]['knight'])
    
def is_opposite_bishop(piece, player):
    return piece == Piece(opposite_piece[player]['bishop'])

def is_opposite_queen(piece, player):
    return piece == Piece(opposite_piece[player]['queen'])

def is_opposite_rook(piece, player):
    return piece == Piece(opposite_piece[player]['rook'])

def is_opposite_king(piece, player):
    return piece == Piece(opposite_piece[player]['king'])

def is_opposite_pawn(piece, player):
    return piece == Piece(opposite_piece[player]['pawn'])

def is_opposite_queen_or_bishop(piece, player):
    return is_opposite_bishop(piece, player) or is_opposite_queen(piece, player)

def is_opposite_queen_or_rook(piece, player):
    return is_opposite_rook(piece, player) or is_opposite_queen(piece, player)