from constants import *

class Piece:
    def __init__(self, team):
        self.team = team
        self.has_moved = False
        self.moved_last = False
        self.row = None
        self.column = None

        # each direction in format (dir_x, dir_y, max_length_in_direction)
        self.single_moves = []
        self.directional_moves = []
        self.orientation = -1 if team == WHITE else 1  # orients pawns by team -- other pieces have symmetry

    def move(self, row, column, board):
        self.row = row
        self.column = column
        self.has_moved = True
        self._reset_moves()
        reachable_squares, blocked_squares = self.get_reachable_and_blocked_coords(board)
        self.set_moves(reachable_squares, blocked_squares)
    
    def _reset_moves(self):
        self.reachable_squares = []
        self.blocked_squares = []

    def set_moves(self, reachable_squares, blocked_squares):
        self.reachable_squares = reachable_squares
        self.blocked_squares = blocked_squares

    def get_reachable_and_blocked_coords(self, board):
        if self.has_moved:
            reachable_squares, blocked_squares = self._get_reachable_and_blocked_squares(board)
        else:
            reachable_squares, blocked_squares = self.on_first_move(board)
        return reachable_squares, blocked_squares

    # TODO: Refactor, a bit repetitive and messy
    def _get_reachable_and_blocked_squares(self, board):
        reachable_squares = []
        blocked_squares = []
        for direction in self.directional_moves:
            can_continue = True
            for distance in range(1, 1 + BOARD_DIM):
                row, column = self._get_square_from_vector(direction, distance)
                if not self._legal_move(row, column, board):
                    break

                if self._reachable_or_blocked(row, column, board) and can_continue:
                    reachable_squares.append((row, column))
                else:
                    blocked_squares.append((row, column))

                # I don't like this, since team is already calculated in _reachable_or_blocked
                square = board[row][column]
                team = self._team_from_square(square)

                # must come after _can_reach_square
                if not self._can_go_further(team):
                    if can_continue:
                        can_continue = False
                    else:
                        break
            
        for single_move in self.single_moves:
            row, column = self._get_square_from_vector(single_move, 1)

            if not self._legal_move(row, column, board):
                continue

            if self._reachable_or_blocked(row, column, board):
                reachable_squares.append((row, column))
            else:
                blocked_squares.append((row, column))
        
        return reachable_squares, blocked_squares

    def _team_from_square(self, square):
        if square.piece:
            team = square.piece.team
        else:
            team = EMPTY
        return team

    def _reachable_or_blocked(self, row, column, board):
        square = board[row][column]
        team = self._team_from_square(square)
        if self._can_take_square(row, column, team):
            return True
        return False

    def _legal_move(self, row, column, board):
        if self._on_board(row, column):
            return True
        return False
    
    def _on_board(self, row, column):
        if row >= 0 and row < BOARD_ROWS:
            if column >= 0 and column < BOARD_COLUMNS:
                return True
        return False

    def _can_go_further(self, team):
        if team == EMPTY: # piece cannot go to squares when any piece (regardless of team) blocks access
            return True
        return False

    def _get_square_from_vector(self, direction, distance):
        dx = distance * direction[0] * self.orientation
        dy = distance * direction[1] * self.orientation
        
        return self.row + dy, self.column + dx


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # basic behavior for pieces, must redefine for king and pawn
    def on_first_move(self, board):
        return self._get_reachable_and_blocked_squares(board)

    def _can_take_square(self, row, column, team):
        if team == self.team:
            return False
        return True

    def on_turn_end(self):
        pass

class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wp.png'
        else:
            self.image = 'images/bp.png'
        self.single_moves = [(0,1), (1,1), (-1,1)]

    def on_first_move(self, board):
        reachable_squares, blocked_squares = self._get_reachable_and_blocked_squares(board)
        
        if not reachable_squares:
            return reachable_squares, blocked_squares

        square = reachable_squares[0]
        two_move_row = square[0] + self.orientation 
        two_move_column = square[1] # column doesn't change

        if self._legal_move(two_move_row, two_move_column, board):
            if self._reachable_or_blocked(two_move_row, two_move_column, board):
                reachable_squares.append((two_move_row, two_move_column))
            else:
                blocked_squares.append((two_move_row, two_move_column))

        return reachable_squares, blocked_squares

    # must be other team piece on forward facing diagonal of pawn
    # diagonals will count as blocked until opposing piece in square
    def _can_take_square(self, row, column, team):
        other_team_on_square = (team != self.team and team != EMPTY)

        # forward move logic
        if team == EMPTY and self.column == column:
            return True

        # diagonal take logic
        if other_team_on_square and self._is_diagonal_of_pawn(row, column):
            return True
        return False

    def _is_diagonal_of_pawn(self, row, column):
        if column == (self.column + 1) or column == (self.column - 1):
            if row == (self.row + self.orientation):
                return True
        return False

class Rook(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wR.png'
        else:
            self.image = 'images/bR.png'
        self.directional_moves = [(1,0),(0,1),(-1,0),(0,-1)]

class Knight(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wN.png'
        else:
            self.image = 'images/bN.png'
        self.single_moves = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

class Bishop(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wB.png'
        else:
            self.image = 'images/bB.png'
        self.directional_moves = [(1,1),(1,-1),(-1,1),(-1,-1)]

class Queen(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wQ.png'
        else:
            self.image = 'images/bQ.png'
        self.directional_moves = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

class King(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wK.png'
        else:
            self.image = 'images/bK.png'
        self.single_moves = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]