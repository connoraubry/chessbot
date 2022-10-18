from game.tools.constants import *
'''
Checks if algebraic coordinate is valid
[a-h][1-8]
'''
def is_coordinate_valid(coordinate):
    if not type(coordinate) == str:
        return False
    if len(coordinate) != 2:
        return False 
    if coordinate[0] not in valid_files:
        return False 
    if coordinate[1] not in valid_ranks:
        return False 
    return True 


def rank_and_file(n):
    return n // 8, n % 8

def index_to_coordinate(index: int):
    file = index % 8
    rank = (index-file) // 8
    return idx_to_file[file] + idx_to_rank[rank]

def coordinate_to_index(coordinate: str):
    file = file_to_idx[coordinate[0]]
    rank = rank_to_idx[coordinate[1]]
    return file + (rank * 8)

def player_of_piece(piece):
    if piece == None:
        return 'n'
    if piece == piece.lower():
        return 'b'
    return 'w'