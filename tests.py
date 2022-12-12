
"""
    Test functionality of chess game with Pytest (and practice TDD)
    Past game data sourced from https://www.kaggle.com/datasets/datasnaek/chess and
    https://github.com/SebLague/Chess-AI/blob/main/Assets/Book/Games.txt
    At best past game data will give me general overview of how well my functions work
    more of statistical confidence than true confidence... other tests needed later...
"""

from constants import *
from board import Board

import pytest
# import pandas as pd
# game_notes = pd.read_csv('games.csv')

# test_board = Board()


"""
    Requires quick way to initialize board from a mid game position
    Quick way to populate moves for pieces (etc.)
"""


def parse_game_notes(notation):
    inputs = []
    expected_results = []
    for turn, move_notation in enumerate(notation.split()):  # notation is algebraic chess notation with each move separated by space
        current_board = get_board(inputs)   # build board off of all previous boards

        # goal of unit test will be to find if the move from game is possible on that board according to my code
        start_position, end_position, piece_type, move_type, causes_check, game_ends_how_or_continues = parse_move(current_board, move_notation)
        inputs.append(
            {
                'current_board':current_board,
                'turn':turn,
                'start_position':start_position,
                'end_position':end_position,
            }
        )
        expected_results.append(
            {
                'piece_type':piece_type,
                'move_type':move_type,
                'causes_check':causes_check,
                'ends_game':game_ends_how_or_continues
            }
        )

        if game_ends_how_or_continues != 'continues':
            break
    
    return inputs, expected_results

# reuses already parsed turns
def get_board(past_inputs):
    if past_inputs:
        pass
    else:
        pass # make starting board

def parse_move(current_board, move):
    pass

def results_in_check(move):
    pass

def get_start_position(current_board, move):
    pass

def get_end_position(current_board, move):
    pass

def get_piece_type(move):
    pass

def get_move_type(current_board, move):
    pass

def continues_or_ends(move):
    pass

def ends_how(move):
    pass
    
def game_note_loader(path = 'games.txt'):
    with open(path, 'r') as file:
        for game_notes in file.readlines():
            yield game_notes

from tqdm import tqdm
def run_tests():
    # track which move types succeed vs fail

    for game_notes in tqdm(game_note_loader()):
        inputs, expected_outputs = parse_game_notes(game_notes)

        for i, input in enumerate(inputs):
            board = populate_board(input['current_board'])
            output = do_move(board, input)



if __name__ == '__main__':
    run_tests()