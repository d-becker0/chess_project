"""
    keep track of all constants
"""

# Dictionary keys 

BLACK = 'black'
WHITE = 'white'

DIRECTION = 'direction'
MAX_DISTANCE = 'scalar'

ROOK = 'r'
KNIGHT = 'n'
BISHOP = 'b'
QUEEN = 'q'
KING = 'k'
PAWN = 'p'
EMPTY = '-'

# Board constants

BOARD_ROWS = 8
BOARD_COLUMNS = 8
if BOARD_ROWS > BOARD_COLUMNS:
    BOARD_DIM = BOARD_ROWS
else:
    BOARD_DIM = BOARD_COLUMNS

# Pygame constants

WIDTH = 512
HEIGHT = 512

        # yes, making assumptions here
SQUARE_SIZE = WIDTH // BOARD_ROWS

# Color constants 

BLACK_COLOR = (10,10,10)
WHITE_COLOR = (230,230,230)

DARK_SQUARE_COLOR = (100, 100, 180)
LIGHT_SQUARE_COLOR = (170, 170, 250)

PRIMARY_HIGHLIGHT = (100, 200, 100)
SECONDARY_HIGHLIGHT = (60, 160, 60)
TERTIARY_HIGHLIGHT = (30, 130, 30)