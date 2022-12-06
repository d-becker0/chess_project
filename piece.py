from constants import *

class Piece:
    def __init__(self, team):
        self.team = team
        self.has_moved = False
        self.moved_last = False

        # each direction in format {dir_x, dir_y, max_length_in_direction, movement_evaluation_type}
        self.move_template = []
        self.orientation = -1 if team == WHITE else 1  # orients pawns by team -- other pieces have symmetry

    def __repr__(self):
        return f"({self.team} {type(self)})"

    def get_possible_moves_as_x_y_coords(self):
        moves = self._get_x_y_for_directional_moves()
        moves = moves.extend( self._get_x_y_for_single_moves )
        return moves

    def _get_x_y_for_directional_moves(self):
        coord_list = []
        for direction in self.directional_moves:
            for i in range(BOARD_DIM):  # largest dimension of board
                coord_list.append(self._multiply_x_y(direction, i))
        return coord_list

    #TODO: better name
    def _multiply_x_y(self, direction, scalar):
        return ( direction[0] * scalar * self.orientation, direction[1] * scalar * self.orientation)

    def _get_x_y_for_single_moves(self):
        return self.single_moves

    def move(self):
        self.has_moved = True

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
        self.template_moves = [{X_DIR: 1, Y_DIR: 0, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
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
        self.template_moves = [{X_DIR: 1, Y_DIR: 2, MAX_DIST: 1, EVAL_TYPE: STANDARD_MOVE},
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
        self.template_moves = [{X_DIR: 1, Y_DIR: 1, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
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
        self.template_moves = [{X_DIR: 1, Y_DIR: 0, MAX_DIST: BOARD_DIM, EVAL_TYPE: STANDARD_MOVE},
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
