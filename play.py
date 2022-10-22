from game import *
import random 

output_file = "game_output.txt"
quit_commands = [
    'quit', 'quit()'
]

gs = Gamestate()

while True:
    if gs.move == 'w':
        gs.print_board()
        print(gs.get_all_moves())
        move = input("Take a move: ")    
        if move in quit_commands:
            break 
        gs.take_move(move)
    else:
        moves = gs.get_all_moves()
        gs.take_move(random.choice(list(moves)))