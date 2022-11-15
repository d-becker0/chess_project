from constants import *

# class storing data about move
class Move:
    def __init__(self, row, column, direction, distance, piece, can_take, is_legal):
        self.direction = direction
        self.distance = distance
        self.row = row
        self.column = column
        self.piece = piece
        self.can_take = can_take
        self.is_legal = is_legal

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

    def row_col_in_current_moves(self, row, column):
        for move in self.current_moves:
            if (row, column) == (move.row, move.column):
                return True
        return False

    def row_col_in_blocked_moves(self, row, column):
        for move in self.blocked_moves:
            if (row, column) == (move.row, move.column):
                return True
        return False

    def move(self, row, column, board):
        self.place_piece(row, column)
        self.has_moved = True
        current_moves, blocked_moves = self._find_moves(board)
        self._set_moves(current_moves, blocked_moves)

    def place_piece(self, row, column):
        self.row = row
        self.column = column
    
    def recalculate_moves(self, board):
        current_moves, blocked_moves = self._find_moves(board)
        self._set_moves(current_moves, blocked_moves)

    def _set_moves(self, current_moves, blocked_moves):
       self.current_moves = current_moves 
       self.blocked_moves = blocked_moves

    def _get_current_and_blocked_moves(self, board):
        if self.has_moved:
            current_moves, blocked_moves = self._find_moves(board)
        else:
            current_moves, blocked_moves = self.on_first_move(board)
        return current_moves, blocked_moves

    # TODO: Refactor, a bit repetitive and messy
    def _find_moves(self, board):
        current_moves = []
        blocked_moves = []
        for direction in self.directional_moves:
            can_continue = True
            for distance in range(1, 1 + BOARD_DIM):
                row, column = self._get_square_from_vector(direction, distance)
                
                # remaining distances are off board too
                if not self._on_board(row, column):
                    break

                results_in_check = False #self._results_in_check(row, column, board)

                square = board[row][column]
                square_team = self._team_from_square(square)

                can_take = self._can_take_square(row, column, square_team)
                
                if can_take and can_continue:
                    current_moves.append(Move(row, column, direction, distance, self, can_take, results_in_check))
                else:
                    blocked_moves.append(Move(row, column, direction, distance, self, can_take, results_in_check))

                # once it can't continue, will remain false for rest of direction
                if can_continue:
                    can_continue = self._can_continue(square_team)
            
        for direction in self.single_moves:
            row, column = self._get_square_from_vector(direction, 1)

            if not self._on_board(row, column):
                continue

            results_in_check = False #self._results_in_check(row, column, board)

            square = board[row][column]
            square_team = self._team_from_square(square)

            can_take = self._can_take_square(row, column, square_team)
            
            if can_take:
                current_moves.append(Move(row, column, direction, 1, self, can_take, results_in_check))
            else:
                blocked_moves.append(Move(row, column, direction, 1, self, can_take, results_in_check))

        return current_moves, blocked_moves

    def _results_in_check(self, row, column, board):
        if not self.king:
            self.king = self._find_king(board)
        king_square = board[self.king.row][self.king.column]
        
        no_check = True
        if self._moves_out_of_pin(row,column,board,king_square):
            pass
        
        if self._not_blocking_check(row,column,board,king_square):
            return True

        return False

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

    def _can_continue(self, team):
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
        return self._find_moves(board)

    def _can_take_square(self, row, column, team):
        if team == self.team:
            return False
        return True

class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team)
        if team == WHITE:
            self.image = 'images/wp.png'
        else:
            self.image = 'images/bp.png'
        self.single_moves = [(0,1), (1,1), (-1,1)]

    def on_first_move(self, board):
        current_moves, blocked_moves= self._find_moves(board)
        
        if not current_moves:
            return current_moves, blocked_moves

        square = current_moves[0]
        two_move_row = square[0] + self.orientation 
        two_move_column = square[1] # column doesn't change

        if self._legal_move(two_move_row, two_move_column, board):
            if self._reachable_or_blocked(two_move_row, two_move_column, board):
                current_moves.append((two_move_row, two_move_column))
            else:
                blocked_moves.append((two_move_row, two_move_column))

        return current_moves, blocked_moves

    # must be other team piece on forward facing diagonal of pawn
    # diagonals will count as blocked until opponent piece in square
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