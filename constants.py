"""
    keep track of all constants
"""

# Dictionary keys 

# teams
BLACK = 'black'
WHITE = 'white'

# move template format
X_DIR = 'x_direction'
Y_DIR = 'y_direction'
DIRECTION = 'direction'  # TODO: likely redundant must check
MAX_DIST = 'scalar'
EVAL_TYPE = 'eval_type'

# specific eval types
STANDARD_MOVE = 'reg'

KING_MOVE = 'king_reg'
CASTLING = 'castle'

PAWN_ATTACK = 'pawn_diagonal'
PAWN_DOUBLE = 'pawn_double'
PROMOTION = 'promote'
EN_PASSANT = 'en_passant'

# piece type
ROOK = 'r'
KNIGHT = 'n'
BISHOP = 'b'
QUEEN = 'q'
KING = 'k'
PAWN = 'p'
EMPTY = '-'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Board constants

BOARD_ROWS = 8
BOARD_COLUMNS = 8

    # larger dimension
if BOARD_ROWS > BOARD_COLUMNS:
    BOARD_DIM = BOARD_ROWS
else:
    BOARD_DIM = BOARD_COLUMNS

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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