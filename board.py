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

    def find_possible_moves(self, turn):
        team = self.turn_to_team(turn)
        oreintation = 1
        if team == BLACK:
            orientation = -1
        
        for piece in self.board.get_pieces():
            
            if piece.team != team:
                continue
            
            row, column = piece.get_position()
            directions = piece.get_directions()
            scalars = piece.get_scalars()
            special_moves = piece.get_specialset()

            possible_moves = []
            for direction in directions:
                x, y = direction

                for scalar in scalars:
                    row_change = orientation*scalar*y
                    col_change = orientation*scalar*x

                    row_w_change = row_change + row
                    col_w_change = col_change + column
                    if self.board.on_board(row_w_change, col_w_change):
                        if self.board.is_empty(row_w_change, col_w_change):
                            possible_moves.append(row_w_change, col_w_change)
                        else:
                            




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


    def get_pieces(self):
        return self.pieces
    
    def remove_piece(self, piece):
        self.pieces.remove(piece)