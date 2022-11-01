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

def rank_file_to_index(rank, file):
    return (rank * 8) + file 

def rank_and_file(n):
    return n // 8, n % 8

def index_to_coordinate(index):
    if type(index) != int:
        return '-'
    if index < 0 or index > 63:
        return '-'
    file = index % 8
    rank = (index-file) // 8
    return idx_to_file[file] + idx_to_rank[rank]

def coordinate_to_index(coordinate: str):
    if coordinate[0] == '-':
        return -1 
    file = file_to_idx[coordinate[0]]
    rank = rank_to_idx[coordinate[1]]
    return file + (rank * 8)

def c2idx(coords):
    return coordinate_to_index(coords)

def player_of_piece(piece):
    if piece == None:
        return 'n'
    return piece.player