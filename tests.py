
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

test_board = Board()

def 