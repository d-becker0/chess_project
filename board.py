from constants import *

class Square:
    def __init__(self):
        self.content = None
        self.blocked_for_pieces = []
        self.reached_by_pieces = []

    def square_is_blocked(self, piece):
        if piece in self.blocked_for_pieces:
            return True
        return False
    
    def square_is_reachable(self, piece):
        if piece in self.reached_by_pieces:
            return True
        return False

    def square_in_moveset(self, piece):
        if self.square_is_blocked(piece) or self.square_is_reachable(piece):
            return True
        return False

class Board:
    def __init__(self):
        self.piece_forepattern = [  PAWN  for board_square in range(BOARD_ROWS)  ]
        self.piece_backpattern = [  ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK  ]

        self.pieces = []

        self.board = []

        self._setup_board()

    # board setup
    def _setup_board(self):
        middle_rows = BOARD_ROWS - 2

        # top row
        self.board.append(self._initialize_row(self.piece_backpattern, BLACK))
        # 2nd to top row
        self.board.append(self._initialize_row(self.piece_forepattern, BLACK))

        for i in range(2, middle_rows):
            
            self.board.append([   setup_square(EMPTY, EMPTY) for j in range(BOARD_COLUMNS)   ])
        
        self.board.append(self._initialize_row(self.piece_forepattern, WHITE))
        self.board.append(self._initialize_row(self.piece_backpattern, WHITE))

    def _initialize_row(self, pattern, team):
        row = []
        for piece_type in pattern:

            piece = setup_square(piece_type,team)
            row.append(piece)
            self.pieces.append(piece)

        return row

    def yield_coords_and_content(self):
        for row_val, row in enumerate(self.board):
            for col_val, square in enumerate(row):
                yield row_val, col_val, square.content

# a bit uggo. 
from piece import Pawn, Rook, Knight, Bishop, Queen, King
piece_switch = {PAWN: Pawn, ROOK: Rook, KNIGHT: Knight, BISHOP: Bishop, QUEEN: Queen, KING: King}
def _fill_square(piece_type, team):
    return piece_switch[piece_type](team)

def setup_square(piece_type, team):
    square = Square()
    if piece_type != EMPTY:
        square.content = _fill_square( piece_switch[piece_type](team) )
    return square