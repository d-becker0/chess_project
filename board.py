from constants import *
from piece import PieceMaker

class SquareMaker:
    def __init__(self):
        self.piece_maker = PieceMaker()

    def make_square(self, team, piece_type):
        piece = self.piece_maker.make_piece(team, piece_type)
        return Square(piece)

class Square:
    def __init__(self, piece):
        self.piece = piece

        self.moves_attacking_square = []
        self.moves_blocked_from_attacking_square = []

class Board:
    def __init__(self):
        self.piece_forepattern = [  PAWN  for board_square in range(BOARD_ROWS)  ]
        self.piece_backpattern = [  ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK  ]

        self.pieces = []

        self.board = []

        self.square_maker = SquareMaker()

        self._setup_board()

    # board setup
    def _setup_board(self):
        middle_rows = BOARD_ROWS - 2

        # top row
        self.board.append(self._initialize_row(self.piece_backpattern, BLACK))
        # 2nd to top row
        self.board.append(self._initialize_row(self.piece_forepattern, BLACK))

        for i in range(2, middle_rows):   # creates 4 empty rows
            
            self.board.append([   self.square_maker.make_square(EMPTY, EMPTY) for j in range(BOARD_COLUMNS)   ])
        
        self.board.append(self._initialize_row(self.piece_forepattern, WHITE))
        self.board.append(self._initialize_row(self.piece_backpattern, WHITE))
    
    def _initialize_row(self, pattern, team):
        row = []
        for piece_type in pattern:

            square = self.square_maker.make_square(team, piece_type)
            row.append(square)
            self.pieces.append(square.piece)
        return row

    def yield_coords_and_piece(self):
        for row_count, row in enumerate(self.board):
            for col_count, square in enumerate(row):
                yield row_count, col_count, square.piece