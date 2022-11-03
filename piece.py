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
        self.orientation = 1 if team == WHITE else -1  # orients pawns by team -- other pieces have symmetry

    def move(self, row, column, board):
        self.row = row
        self.column = column
        self._reset_moves()
        self.calculate_and_set_moves(board)
    
    def _reset_moves(self):
        self.reachable_moves = []
        self.blocked_moves = []

    def _set_moves(self, reachable_squares, blocked_squares):
        print(reachable_squares)
        print(blocked_squares)
        self.reachable_squares = reachable_squares
        self.blocked_squares = blocked_squares

    def calculate_and_set_moves(self, board):
        if self.has_moved:
            reachable_squares, blocked_squares = self._get_reachable_and_blocked_squares(board)
        else:
            reachable_squares, blocked_squares = self.on_first_move(board)
        self._set_moves(reachable_squares, blocked_squares)

    def _get_reachable_and_blocked_squares(self, board):
        reachable_squares = []
        blocked_squares = []
        for direction in self.directional_moves:
            can_continue = True
            for distance in range(BOARD_DIM):
                row, column = self._get_square_from_vector(direction, distance)
                if not self._on_board(row, column):
                    continue

                square = board[row][column]
                team = self._team_from_square(square)

                # only reachable if other team / empty and hasn't encountered side 
                # and hasn't hit piece of same team
                if self._can_take_square(team) and can_continue:
                    reachable_squares.append((row, column))
                else:
                    blocked_squares.append((row, column))

                # must come after _can_reach_square
                if not self._can_go_further(team):
                    can_continue = False
            
        for single_move in self.single_moves:
            row, column = self._get_square_from_vector(single_move, 1)
            if not self._on_board(row, column):
                continue

            square = board[row][column]
            team = self._team_from_square(square)
            if self._can_take_square(team):
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
    
    def _on_board(self, row, column):
        if row >= 0 and row < BOARD_ROWS:
            if column >= 0 and column < BOARD_COLUMNS:
                return True
        return False

    def _can_take_square(self, team):
        if team == self.team:
            return False
        return True

    def _can_go_further(self, team):
        if team == EMPTY: # piece cannot go to squares when any piece (regardless of team) blocks access
            return True
        return False

    def _get_square_from_vector(self, direction, distance):
        dx = distance * direction[0] * self.orientation
        dy = distance * direction[1] * self.orientation
        
        return self.row + dy, self.column + dx

    # basic behavior for pieces, must redefine for king and pawn
    def on_first_move(self, board):
        return self._get_reachable_and_blocked_squares(board)

    def on_turn_end(self):
        pass

class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wp.png'
        else:
            self.image = 'images/bp.png'
        self.single_moves = [(0,1)]

        def on_first_move(self, board):
            pass

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