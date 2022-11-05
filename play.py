from game import *
from chessbot import eval
import random 

output_file = "game_output.txt"
quit_commands = [
    'quit', 'quit()'
]

g = Game()
with open('output.pgn', 'w') as fp:
    count = 1
    while True:
        if g.move == Player.WHITE:
            g.print_board()
            moves = g.get_all_moves()
            if len(moves) == 0 and g.board.white_in_check:
                print("Checkmate black!")
                break
            print(moves)
            
            move = input("Take a move: ")    
            if move in quit_commands:
                break 
            if move in moves:
                g.take_move(move)
                fp.write('{}. {} '.format(count, move))
            if '#' in move:
                break 
        else:
            moves = g.get_all_moves()
            print("black", moves)
            if len(moves) == 0 and g.board.black_in_check:
                print("Checkmate white!")
                break 

            smallest_score = 10000000
            move_choice = None
            for move in moves:
                g.take_move(move)
                score = eval.calculate_score(g)
                if score < smallest_score:
                    move_choice = move 
                    smallest_score = score 
                g.undo_move()
            
            g.take_move(move)
            fp.write('{}\n'.format(move))
            if '#' in move:
                break 
            count += 1
g.print_board()
print("Game over")