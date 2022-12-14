
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

from tqdm import tqdm
def run_tests():
    # track which move types succeed vs fail

    for game_notes in tqdm(game_note_loader()):
        inputs, expected_outputs = parse_game_notes(game_notes)

        for input, expected_output in zip(inputs, expected_outputs):
            board = populate_board(input['current_board'])
            try:
                output = do_move(board, input)
            except:
                output = 'Error'
                print('move results in error for code')

            comparison = compare(output, expected_outputs)

            track_comparison(comparison)

    print_test_output()


if __name__ == '__main__':
    run_tests()