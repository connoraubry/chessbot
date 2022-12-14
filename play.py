from game import *
from chessbot import eval
import random 

output_file = "game_output.txt"
quit_commands = [
    'quit', 'quit()'
]

gs = Gamestate()
with open('output.pgn', 'w') as fp:
    count = 1
    while True:
        if gs.move == Player.WHITE:
            gs.print_board()
            moves = gs.get_all_moves()
            if len(moves) == 0 and gs.board.white_in_check:
                print("Checkmate black!")
                break
            print(moves)
            
            move = input("Take a move: ")    
            if move in quit_commands:
                break 
            if move in moves:
                gs.take_move(move)
                fp.write('{}. {} '.format(count, move))
            if '#' in move:
                break 
        else:
            moves = gs.get_all_moves()
            print("black", moves)
            if len(moves) == 0 and gs.board.black_in_check:
                print("Checkmate white!")
                break 

            smallest_score = 10000000
            move_choice = None
            for move in moves:
                real_move = gs.string_to_move[move]
                gs.temp_move(real_move)
                score = eval.calculate_score(gs)
                if score < smallest_score:
                    move_choice = move 
                    smallest_score = score 
                gs.reverse_temp_move(real_move)
            
            gs.take_move(move)
            fp.write('{}\n'.format(move))
            if '#' in move:
                break 
            count += 1
gs.print_board()
print("Game over")