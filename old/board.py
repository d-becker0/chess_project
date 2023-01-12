from old.constants import *
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
    def __init__(self, fen_string = None):
        # self.piece_forepattern = [  PAWN  for board_square in range(BOARD_ROWS)  ]
        # self.piece_backpattern = [  ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK  ]
        setup_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        
        if fen_string:
            setup_fen = fen_string

        self.pieces = []

        self.square_maker = SquareMaker()

        self.board = self._set_up_board_from_FEN(setup_fen)

    # # board setup
    # def _setup_board(self):
    #     middle_rows = BOARD_ROWS - 2

    #     # top row
    #     self.board.append(self._initialize_row(self.piece_backpattern, BLACK))
    #     # 2nd to top row
    #     self.board.append(self._initialize_row(self.piece_forepattern, BLACK))

    #     for i in range(2, middle_rows):   # creates 4 empty rows
            
    #         self.board.append([   self.square_maker.make_square(EMPTY, EMPTY) for j in range(BOARD_COLUMNS)   ])
        
    #     self.board.append(self._initialize_row(self.piece_forepattern, WHITE))
    #     self.board.append(self._initialize_row(self.piece_backpattern, WHITE))
    
    # def _initialize_row(self, pattern, team):
    #     row = []
    #     for piece_type in pattern:

    #         square = self.square_maker.make_square(team, piece_type)
    #         row.append(square)
    #         self.pieces.append(square.piece)

    #     return row

    def _create_row(self, row_patterns):
        for row in row_patterns:

            for square_value in row:
                
                square = self.square_maker.make_square(square_value[0], square_value[1])
                row.append(square)
                self.pieces.append(square.piece)

        return row

    def yield_coords_and_piece(self):
        for row_count, row in enumerate(self.board):
            for col_count, square in enumerate(row):
                yield row_count, col_count, square.piece

    def _translate_fen_to_row(self, fen_string):
        char_to_piece = {'p':PAWN, 'r': ROOK, 'n': KNIGHT, 'b':BISHOP, 'q':QUEEN, 'k':KING}
        row_patterns = []
        for char in fen_string:
            row = []
            if char.isnumeric():
                row.append( (EMPTY, EMPTY) for i in range( int(char) )  )

            elif char.isalpha():
                if char.islower():
                    team = BLACK
                else:
                    team = WHITE
                
                piece = char_to_piece[char.lower()]

                row.append( ( team, piece ) )

            elif char == '/':
                row_patterns.append(row)

            else:
                print('character:', char, 'couldn\'t be translated')
                break

        return row_patterns

    def _set_up_board_from_FEN(self, fen_string):
        board = []

        row_patterns = self._translate_fen_to_row(fen_string)
        
        for row_pattern in row_patterns:
            board.append(self._create_row(row_pattern))

        #self.board = fen_board
        return board