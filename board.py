from keys import *
from piece import make_piece

class Game:
    def __init__(self, board):
        self.turn = 0
        self.board = board

    def turn_to_team(self, turn):
        if turn%2:
            return WHITE
        else: 
            return BLACK

    # for all pieces of a certain team, return valid moves for that turn
        # valid move = legal for piece type and does not result in check
    def get_team_moves(self, team):
        team_moves = []
        for (row, col), piece in self.board.yield_coords_and_content():
            if piece.team == team:
                move = self.get_piece_moves(row, col, piece)
                if move:
                    team_moves.extend(move)
        
        return team_moves
                    

    def get_piece_moves(self, row, col, piece):
        valid_moves = []
        for move in piece.yield_possible_moves():
            self.board.check_move(piece, move)
        

class Board:
    def __init__(self):
        self.piece_forepattern = [  PAWN  for board_square in range(BOARD_ROWS)  ]
        self.piece_backpattern = [  ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK  ]

        self.pieces = []

        self.current_board = []
        self.past_boards = []

        self._place_pieces()

    # board setup
    def _place_pieces(self):
        middle_rows = BOARD_ROWS - 2

        # top row
        self.current_board.append(self._initialize_row(self.piece_backpattern, BLACK))
        # 2nd to top row
        self.current_board.append(self._initialize_row(self.piece_forepattern, BLACK))

        for i in range(2, middle_rows):
            
            self.current_board.append([   make_piece(EMPTY, EMPTY) for j in range(BOARD_COLUMNS)   ])
        
        self.current_board.append(self._initialize_row(self.piece_forepattern, WHITE))
        self.current_board.append(self._initialize_row(self.piece_backpattern, WHITE))

    def _initialize_row(self, pattern, team):
        row = []
        for piece_type in pattern:

            piece = make_piece(piece_type,team)
            row.append(piece)
            self.pieces.append(piece)

        return row

    def yield_coords_and_content(self):
        for row_val, row in enumerate(self.current_board):
            for col_val, content in enumerate(row):
                yield (row_val,col_val), content

    def remove_piece(self, piece):
        self.pieces.remove(piece)