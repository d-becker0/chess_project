from old.constants import *

class CheckLogic:
    """
        Class which defines basic check logic
    """
    def __init__(self, team, king):
        self.team = team
        self.king = king

    def in_check(self):
        pass

class KingCheckLogic:
    """
        Class which defines basic check logic for king
    """
    pass
    
class LogicMaker:
    def __init__(self):
        # TODO: reuse classes

        self.string_to_class = {
            STANDARD_MOVE: MoveLogic(CheckLogic()),
            KING_MOVE: MoveLogic(KingCheckLogic()),
            # CASTLING: (CastlingLogic, CastlingCheckLogic)
            PAWN_ATTACK: PawnAttackMoveLogic(CheckLogic()),
            PAWN_DOUBLE: PawnDoubleMoveLogic(CheckLogic()),
            # PROMOTION: (PawnPromoteLogic, CheckLogic),
            # EN_PASSANT: (PawnEnpassantMoveLogic, EnpassantCheckLogic)
        }
    
    def _change_string_to_class(self, string):
        return self.string_to_class(string)

    def make(self, string, *args, **kwargs):
        return MoveLogic(CheckLogic()) #self._change_string_to_class[string](*args, **kwargs)

# Needs to return a move object which 
class MoveLogic:
    def __init__(self, check_logic_instance):
        self.check_logic = check_logic_instance  # this needs to know the board, piece, and king of piece team

    def _results_in_check(self, template_move_on_board, board):
        return self.check_logic.in_check(template_move_on_board, board)
    
    # Keep in mind, this needs access to the board the piece
    def _parse_template(self, template, board):
        pass

    def evaluate_template(self, template, board):
        template_move_on_board = self._parse_template(template)

class PawnDoubleMoveLogic:
    pass

class PawnAttackMoveLogic:
    pass

class PawnEnpassantMoveLogic:
    pass

class Move:
    """
        Stores move information and function for when it needs to be reevaluated
    """
    def __init__(self, to_row, to_column, x_dir, y_dir, distance, 
                 piece, can_take, is_legal, pieces_in_between, update_function):
                 
        self.to_row = to_row
        self.to_column = to_column

        self.x_dir = x_dir
        self.y_dir = y_dir
        self.distance = distance

        self.piece = piece

        self.can_take = can_take
        self.is_legal = is_legal
        self.pieces_in_between = pieces_in_between

        self.update_function = update_function

    def update(self):
        self.update_function()
        
    def __repr__(self):
        return f"{self.can_take} at ({self.to_row}, {self.to_column})"

    def __eq__(self, other_move):
        return (self.to_row, self.to_column) == (other_move.to_row, other_move.to_column)


    def _find_moves(self, board):
        current_moves = []
        blocked_moves = []
        for direction in self.directional_moves:
            can_continue = True
            pieces_in_between = 0
            for distance in range(1, 1 + BOARD_DIM):
                row, column = self._get_square_from_vector(direction, distance)
                
                # remaining distances are off board too
                if not self._on_board(row, column):
                    break

                results_in_check = self._results_in_check(row, column, board)

                square = board[row][column]
                square_team = self._team_from_square(square)

                can_take = self._can_take_square(row, column, square_team)
                
                if can_take and not results_in_check and can_continue:
                    current_moves.append(Move(row, column, direction, distance, self, can_take, results_in_check, pieces_in_between))
                else:
                    blocked_moves.append(Move(row, column, direction, distance, self, can_take, results_in_check, pieces_in_between))

                # once it can't continue, will remain false for rest of direction
                if can_continue:
                    can_continue = self._can_continue(square_team)

                # keep track of how many pieces are between current piece and square
                if square.piece:
                    pieces_in_between +=1
            
        for direction in self.single_moves:
            pieces_in_between = 0
            row, column = self._get_square_from_vector(direction, 1)

            if not self._on_board(row, column):
                continue

            results_in_check = self._results_in_check(row, column, board)

            square = board[row][column]
            square_team = self._team_from_square(square)

            can_take = self._can_take_square(row, column, square_team)

            if can_take and not results_in_check:
                current_moves.append(Move(row, column, direction, 1, self, can_take, results_in_check, pieces_in_between))
            else:
                blocked_moves.append(Move(row, column, direction, 1, self, can_take, results_in_check, pieces_in_between))

        return current_moves, blocked_moves

    # TODO: Am not yet considering illegal moves which cause checks
    def _results_in_check(self, row, column, board):
        king_square = self._find_king(board)
        checking_moves = self._get_checking_moves(king_square)

        check = True
        
        blocked_moves = [move for move in king_square.blocked_for_pieces if move.piece.team != self.team]
        leaving_pin = not isinstance(self, King) and self._moves_out_of_pin(row,column,board, blocked_moves)
        
        blocking = not isinstance(self, King) and self._blocking_check(row, column, checking_moves)

        fleeing = isinstance(self, King) and self._fleeing_check(row, column, board)

        checking_pieces = [move.piece for move in checking_moves if move.piece.team != self.team]
        taking = self._takes_checking_piece(row, column, checking_pieces)
        
        if (fleeing or blocking or taking) and not leaving_pin:
            return False
        else:
            return True

    def _get_checking_moves(self, king_square):
        checking_moves = []
        for move in king_square.reached_by_pieces:
            if move.piece.team == self.team:
                continue
            else:
                checking_moves.append(move)
        return checking_moves

    # will only apply to non-king pieces
    def _moves_out_of_pin(self, row, column, board, blocked_moves):
        self_square = board[self.row][self.column]
        pieces_which_reach_self = [move.piece for move in self_square.reached_by_pieces if move.piece.team != self.team]

        leaving_pin = False
        for move in blocked_moves:  # blocked moves are from king square
            if move.piece.team != self.team and move.piece in pieces_which_reach_self:
                # don't care about moves of same team that don't have current move to piece (no check possible)
                leaving_pin = True

                if move.pieces_in_between <= 1:
                    for current_move in move.piece.current_moves: # moving towards pinning piece (on "line" between king and pinning piece)
                        if (row, column) == (current_move.row, current_move.column):
                            leaving_pin = False
                            break
                    for blocked_move in move.piece.blocked_moves:
                        if (row, column) == (blocked_move.row, blocked_move.column) and blocked_move.pieces_in_between ==1:
                            # pieces_in_between ==1, when a pinned piece moves away from pinning piece (towards king)
                            leaving_pin = False
                            break
        return leaving_pin

    # will only apply to king pieces
    def _fleeing_check(self, row, column, board):
        fleeing = True
        for move in board[row][column].reached_by_pieces:
            if move.piece.team != self.team:
                fleeing = False
        return fleeing

    # will only apply to non-king pieces
    def _blocking_check(self, row, column, checking_moves):
        blocking = True
        for checking_move in checking_moves:  # limited to moves before/on the king
            moves_in_check_direction = self._get_current_moves_in_direction(checking_move)

            for dir_move in moves_in_check_direction:
                if (row, column) == (dir_move.row, dir_move.column):
                    blocking = True
                    break
                else:
                    blocking = False

        return blocking

    def _takes_checking_piece(self, row, column, checking_pieces):
        taking = False
        for checking_piece in checking_pieces:
            if (row,column) == (checking_piece.row, checking_piece.column):
                taking = True
            else:
                taking = False
        return taking
            
    def _get_current_moves_in_direction(self, move):
        reachable_moves = []
        for current_move in move.piece.current_moves:
            if move.direction == current_move.direction:
                reachable_moves.append(current_move)
        return reachable_moves

    def _get_blocked_moves_in_direction(self, move):
        blocked_moves = []
        for blocked_move in move.piece.blocked_moves:
            if move.direction == blocked_move.direction:
                blocked_moves.append(blocked_move)
        return blocked_moves

    def _find_king(self, board):
        for row in board:
            for square in row:
                if square.piece and isinstance(square.piece, King) and square.piece.team == self.team:
                    return square
        return None

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

    # row, column are important when using for pawn! DON'T REMOVE!!!
    def _can_take_square(self, row, column, team):
        if team == self.team:
            return False
        return True

class PawnMoveBehavior(MoveBehavior):
    # very lazy hacky way of dealing with this
    def on_first_move(self, board):
        self.single_moves.append((0,2))
        current_moves, blocked_moves = self._find_moves(board)
        self.single_moves.remove((0,2))
        
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