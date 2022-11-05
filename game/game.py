from game.gamestate import Gamestate
from game.tools import * 
from copy import deepcopy

class Game():
    def __init__(self, fen=starting_FEN):
        self.states = [Gamestate(fen)]

    @property
    def state(self):
        return self.states[-1]
    
    @property
    def board(self):
        return self.state.board 
    
    @property
    def move(self):
        return self.state.move 
    
    @property
    def castle(self):
        return self.state.castle

    def get_all_moves(self):
        return self.state.get_all_moves()

    def print_board(self):
        self.state.print_board()

    @property
    def string_to_move(self):
        return self.state.string_to_move

    def take_move(self, string_move):
        if string_move in self.string_to_move:
            newGamestate = deepcopy(self.state)
            move = self.string_to_move[string_move]


            if move.castle is not None:
                newGamestate.take_castle(move)

            else:
                newGamestate.board[move.end] =  move.piece 
                newGamestate.board[move.start] = None                

            if move.en_passant_piece_spot is not None:
                newGamestate.board[move.en_passant_piece_spot] = None

            if move.promotion is not None:
                newGamestate.board[move.end] = move.promotion

            if move.en_passant_revealed_spot is not None:
                newGamestate.en_passant = move.en_passant_revealed_spot
            else:
                newGamestate.en_passant = -1

            if move.piece.is_king():
                if move.piece.is_white():
                    newGamestate.board.white_king = move.end 
                elif move.piece.is_black():
                    newGamestate.board.black_king = move.end 

            #if rook moving at beginning, remove castle possibility 
            if move.piece.is_rook():
                map = {56: 'q', 63: 'K', 0: 'Q', 7: 'K'}
                if move.start in map:
                    newGamestate.castle = newGamestate.castle.replace(map[move.start], '')

            if move.piece.is_pawn() or move.capture is not None:
                newGamestate.halfmove_clock = 0
            else:
                newGamestate.halfmove_clock += 1

            if newGamestate.move == Player.WHITE:
                newGamestate.move = Player.BLACK
            elif newGamestate.move == Player.BLACK:
                newGamestate.move = Player.WHITE

                newGamestate.fullmove_counter += 1
            
            newGamestate.get_all_moves()
            self.states.append(newGamestate)

    def undo_move(self):
        self.states = self.states[:-1]