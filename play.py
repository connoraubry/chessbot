from game import *
import random 

output_file = "game_output.txt"
quit_commands = [
    'quit', 'quit()'
]

gs = Gamestate()
with open('output.pgn', 'w') as fp:
    count = 1
    while True:
        print(gs.board.__dict__)
        if gs.move == Player.WHITE:
            gs.print_board()
            moves = gs.get_all_moves()
            if len(moves) == 0:
                break 
            print(moves)
            
            move = input("Take a move: ")    
            if move in quit_commands:
                break 
            if move in moves:
                gs.take_move(move)
                fp.write('{}. {} '.format(count, move))

        else:
            moves = gs.get_all_moves()
            print("black", moves)
            if len(moves) == 0:
                break 
            move = random.choice(list(moves))
            
            gs.take_move(move)
            fp.write('{}\n'.format(move))
            count += 1