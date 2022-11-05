from constants import *

class Square:
    def __init__(self):
        self.piece = None
        self.blocked_for_pieces = []
        self.reached_by_pieces = []

    # only recalculate moves of pieces that interact with previous and new square
    def get_pieces_to_update(self):
        visited = []
        for piece in self.blocked_for_pieces:
            if piece not in visited:
                visited.append(piece)

                print("Recalculated", piece, "at position", str((piece.row, piece.column)))
                
        for piece in self.reached_by_pieces:
            if piece not in visited:
                visited.append(piece)

                print("Recalculated", piece, "at position", str((piece.row, piece.column)))

        return visited
        
    def reset_subscriptions(self):
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
        self._initialize_piece_moves()
        self._subscribe_pieces_to_squares(self.pieces)


    # TODO: lots of redundancy to reduce

    def update(self, row, column, piece_square):
        piece = piece_square.piece

        new_square = self.board[row][column]

        new_square.piece = piece
        piece_square.piece = None

        piece.move(row, column, self.board)

        update_pieces = new_square.get_pieces_to_update()
        update_pieces.extend( piece_square.get_pieces_to_update() )

        for piece_to_update in update_pieces:
            reachable_squares, blocked_squares = piece_to_update.get_reachable_and_blocked_coords(self.board)
            piece_to_update.set_moves(reachable_squares, blocked_squares)

        new_square.reset_subscriptions()
        piece_square.reset_subscriptions()

        self._subscribe_pieces_to_squares(update_pieces)

        

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
    
    def _initialize_piece_moves(self):
        for row, column, piece in self.yield_coords_and_piece():
            if piece:
                piece.row = row
                piece.column = column
                reachable_squares, blocked_squares = piece.get_reachable_and_blocked_coords(self.board)
                piece.set_moves(reachable_squares, blocked_squares)

    def _subscribe_pieces_to_squares(self, pieces):
        for piece in pieces:
            self._subscribe_single_piece_to_squares(piece)
            
    def _subscribe_single_piece_to_squares(self, piece):
        if piece:
            for (move_row, move_column) in piece.reachable_squares:
                self.board[move_row][move_column].reached_by_pieces.append(piece)
            for (move_row, move_column) in piece.blocked_squares:
                self.board[move_row][move_column].blocked_for_pieces.append(piece)


    def _initialize_row(self, pattern, team):
        row = []
        for piece_type in pattern:

            square = setup_square(piece_type, team)
            row.append(square)
            self.pieces.append(square.piece)

        return row

    def yield_coords_and_piece(self):
        for row_val, row in enumerate(self.board):
            for col_val, square in enumerate(row):
                yield row_val, col_val, square.piece

# a bit uggo. 
from piece import Pawn, Rook, Knight, Bishop, Queen, King
piece_switch = {PAWN: Pawn, ROOK: Rook, KNIGHT: Knight, BISHOP: Bishop, QUEEN: Queen, KING: King}
def _fill_square(piece_type, team):
    return piece_switch[piece_type](team)

def setup_square(piece_type, team):
    square = Square()
    if piece_type != EMPTY:
        square.piece = _fill_square(piece_type, team)
    return square