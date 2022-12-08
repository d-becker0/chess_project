from constants import *

class Piece:
    def __init__(self, team):
        self.team = team
        self.has_moved = False

        self.current_moves = []
        self.invalid_moves = []

        # each direction in format {dir_x, dir_y, max_length_in_direction, movement_evaluation_type}
        self.move_template = []
        self.orientation = -1 if team == WHITE else 1  # orients pawns by team -- other pieces have symmetry

    def __repr__(self):
        return f"({self.team} {type(self)})"

    def move(self):
        self.has_moved = True

    def evaluate_move(self):
        pass

    def _add_move_to_current_moves(self, move):
        pass

    def _delete_move_from_current_moves(self, move):
        pass

    def _add_move_to_invalid_moves(self, move):
        pass

    def _delete_move_from_invalid_moves(self, move):
        pass

# TODO: for now this works, but I don't like the hard-to-parse dict format
# move_template format = {X_DIR:, Y_DIR:, MAX_DIST:, EVAL_TYPE: }
class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wp.png'
        else:
            self.image = 'images/bp.png'
        self.move_template = [{X_DIR: 0, Y_DIR: 1, MAX_DIST: 1, EVAL_TYPE: STANDARD_MOVE},
                              {X_DIR: 0, Y_DIR: 2, MAX_DIST: 1, EVAL_TYPE: PAWN_DOUBLE},
                              {X_DIR: 1, Y_DIR: 1, MAX_DIST: 1, EVAL_TYPE: PAWN_ATTACK},
                              {X_DIR: -1, Y_DIR: 1, MAX_DIST: 1, EVAL_TYPE: PAWN_ATTACK}]

class Rook(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wR.png'
        else:
            self.image = 'images/bR.png'
        self.move_template = [{X_DIR: 1, Y_DIR: 0, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: 0, Y_DIR: 1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: -1, Y_DIR: 0, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: 0, Y_DIR: -1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE}]

class Knight(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wN.png'
        else:
            self.image = 'images/bN.png'
        self.move_template = [{X_DIR: 1, Y_DIR: 2, MAX_DIST: 1, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: 2, Y_DIR: 1, MAX_DIST: 1, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: -1, Y_DIR: 2, MAX_DIST: 1, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: -2, Y_DIR: 1, MAX_DIST: 1, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: -2, Y_DIR: -1, MAX_DIST: 1, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: -1, Y_DIR: -2, MAX_DIST: 1, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: 1, Y_DIR: -2, MAX_DIST: 1, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: 2, Y_DIR: -1, MAX_DIST: 1, EVAL_TYPE: STANDARD_MOVE}]

class Bishop(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wB.png'
        else:
            self.image = 'images/bB.png'
        self.move_template = [{X_DIR: 1, Y_DIR: 1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: -1, Y_DIR: 1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: -1, Y_DIR: -1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: 1, Y_DIR: -1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE}]

class Queen(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wQ.png'
        else:
            self.image = 'images/bQ.png'
        self.move_template = [{X_DIR: 1, Y_DIR: 0, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: 0, Y_DIR: 1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: -1, Y_DIR: 0, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: 0, Y_DIR: -1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: 1, Y_DIR: 1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: -1, Y_DIR: 1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: -1, Y_DIR: -1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
                               {X_DIR: 1, Y_DIR: -1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE}]

class King(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wK.png'
        else:
            self.image = 'images/bK.png'
        self.single_moves = [{X_DIR: 1, Y_DIR: 0, MAX_DIST: 1, EVAL_TYPE: KING_MOVE},
                             {X_DIR: 0, Y_DIR: 1, MAX_DIST: 1, EVAL_TYPE: KING_MOVE},
                             {X_DIR: -1, Y_DIR: 0, MAX_DIST: 1, EVAL_TYPE: KING_MOVE},
                             {X_DIR: 0, Y_DIR: -1, MAX_DIST: 1, EVAL_TYPE: KING_MOVE},
                             {X_DIR: 1, Y_DIR: 1, MAX_DIST: 1, EVAL_TYPE: KING_MOVE},
                             {X_DIR: -1, Y_DIR: 1, MAX_DIST: 1, EVAL_TYPE: KING_MOVE},
                             {X_DIR: -1, Y_DIR: -1, MAX_DIST: 1, EVAL_TYPE: KING_MOVE},
                             {X_DIR: 1, Y_DIR: -1, MAX_DIST: 1, EVAL_TYPE: KING_MOVE}]

class PieceMaker:
    def __init__(self):
        self.string_to_class = {
            PAWN:Pawn, ROOK: Rook, KNIGHT: Knight, BISHOP: Bishop, QUEEN: Queen, KING: King
        }

    def make_piece(self, team, piece_type):  # initializes piece of type 'piece_type'
        piece_class = self._change_string_to_class(piece_type)
        return piece_class(team)

    def _change_string_to_class(self, piece_type):
        return self.string_to_class[piece_type]
