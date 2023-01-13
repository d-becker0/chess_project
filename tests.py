
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
import pandas as pd

def start_test_game():
    pass

def test_piece_moves():
    game_data = pd.read_pickle('test_data/game_info')

    for game_id in game_data['game_id'].unique:
