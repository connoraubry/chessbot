from pathlib import Path 
first_moves = set([l + '3' for l in 'abcdefgh'] + 
                  [l + '4' for l in 'abcdefgh'] + 
                  ['Na3', 'Nc3', 'Nf3', 'Nh3'])


first_black_moves =  set([l + '6' for l in 'abcdefgh'] +
                         [l + '5' for l in 'abcdefgh'] +
                         ['Nc6', 'Na6', 'Nf6', 'Nh6'])

fen_configs = {}
for config in (Path(__file__).parent / "FEN_configs").glob('*'):
    with open(config, 'r') as fp:
        fen_configs[config.stem] = fp.readline()

