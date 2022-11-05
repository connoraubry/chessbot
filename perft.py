from game import Game 


g = Game()
depth = 4


def perft(g, depth):
    count = 0
    if depth == 1:
        return len(g.get_all_moves())

    for move in g.get_all_moves():
        g.take_move(move)
        count += perft(g, depth-1)
        g.undo_move()

    return count 


print(perft(g, depth))