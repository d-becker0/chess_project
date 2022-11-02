from constants import *

class Piece:
    def __init__(self, team):
        self.team = team
        self.has_moved = False
        self.moved_last = False

        # each direction in format (dir_x, dir_y, max_length_in_direction)
        self.directions = []
        self.orientation = 1 if team == WHITE else -1  # orients pawns by team -- other pieces have symmetry

    def initialize_moveset(self, row, column, board):
        self.move_set = self._get_moves(row, column, board)

    def _get_moves(self, row, column, board):
        if self.has_moved:
            reachable_squares, blocked_squares = self._get_reachable_and_blocked_squares(row, column, board)
        else:
            reachable_squares, blocked_squares = self.on_first_move(row, column, board)
        
        return reachable_squares, blocked_squares
        

    def _get_reachable_and_blocked_squares(self, board):
        reachable_squares = []
        blocked_squares = []
        for direction in self.directions:

            can_continue = True
            for distance in range(BOARD_DIM):
                x,y = self._get_squares_from_vector(direction, distance)

                square_content = board.get_square_content(x,y)

                team = square_content.team

                if self._can_reach_square(team):
                    if can_continue:
                        reachable_squares.append((x,y))
                    else:
                        blocked_squares.append((x,y))

                # must come after _can_reach_square
                if not self._can_go_further(team):
                    can_continue = False
            
            return reachable_squares, blocked_squares

    def _can_reach_square(self, team):
        if team == self.team:
            return False
        return True

    def _can_go_further(self, team):
        if team == EMPTY: # piece cannot go to squares when any piece (regardless of team) blocks access
            return True
        return False

    def _get_squares_from_vector(self, direction, distance):
        dx = distance * direction[0] * self.orientation
        dy = distance * direction[1] * self.orientation

        return self.position[0]+dx, self.position[1]+dy

    # basic behavior for pieces, must redefine for king and pawn
    def on_first_move(self, row, column, board):
        return self._get_reachable_and_blocked_squares(row, column, board)

    def on_turn_end(self):
        pass

class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wp.png'
        else:
            self.image = 'images/bp.png'

class Rook(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wR.png'
        else:
            self.image = 'images/bR.png'

class Knight(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wN.png'
        else:
            self.image = 'images/bN.png'

class Bishop(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wB.png'
        else:
            self.image = 'images/bB.png'

class Queen(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wQ.png'
        else:
            self.image = 'images/bQ.png'

class King(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wK.png'
        else:
            self.image = 'images/bK.png'