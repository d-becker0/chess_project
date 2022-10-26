from keys import *

class Piece:
    def __init__(self, team):
        self.team = team
        self.has_moved = False
        self.moved_last = False

        # define moves that can be taken, and piece logic
        # strides are directions a piece can move across the whol board. Ex: rook moves
        # steps are single spaces a piece can move. Ex: King moves
        # specials are special movements. Ex: castling for king, pawn double move
        self.strides = []
        self.steps = []
        self.specials = []

        self.valid_moves = []

    def validate_move(self):
        pass
    
    def is_space_legal(self, square):
        # when square has piece
        if square:
            if square.team == self.team:
                return False
            else:
                return True
        # when square is empty
        return True

    # yield the next square in series for strides. Ex: rook moves 1, rook moves 2, rook moves ...
    # return format is x,y in perspective of piece starting at bottom of board (only matters for pawn, since 1 direction)
    def yield_stride_squares(self, get_new_direction = False):
        for direction in self.strides:
            for scalar in range(1,BOARD_ROWS+1):
                if get_new_direction:
                    break
                yield (scalar*direction[0],scalar*direction[1])
    
    def yield_step_squares(self):
        for step in self.steps:
            yield step

    def yield_specials(self):
        for special in self.specials:
            yield special

    # TODO: this bool probably doesn't work the way I want it to
    def yield_possible_moves(self, get_new_direction = False):
        for stride in self.yield_stride_squares(self, get_new_direction):
            yield stride
        for step in self.yield_step_squares(self):
            yield step
        for special in self.yield_specials(self):
            yield special
    
    # move defined by new coords and piece
    def add_move(self, move):
        self.valid_moves.append(move)

    def move(self):
        self.has_moved = True
        self.moved_last = True

    def on_turn_end(self):
        self.valid_moves = []

class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.strides = []
        self.steps = [(0,1),(1,1),(-1,1)]
        self.specials = [(self.send_enpassant, self.recieve_enpassant), 
                           (self.send_promote, self.recieve_promote)]

    def send_enpassant(self):
        pass
    
    def recieve_enpassant(self):
        pass

    def send_promote(self):
        pass

    def recieve_promote(self):
        pass

class Rook(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.strides = [(1,0),(-1,0),(0,1),(0,-1)]
        self.steps = []
        self.specials = []

class Knight(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.strides = []
        self.steps = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        self.specials = []

class Bishop(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.strides = [(1,1),(1,-1),(-1,-1),(-1,1)]
        self.steps = []
        self.specials = []

class Queen(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.strides = [(1,1),(1,-1),(-1,-1),(-1,1),(1,0),(-1,0),(0,1),(0,-1)]
        self.steps = []
        self.specials = []

class King(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.strides = []
        self.steps = [(1,1),(1,-1),(-1,-1),(-1,1),(1,0),(-1,0),(0,1),(0,-1)]
        self.specials = [(self.send_castle, self.recieve_castle)]

    def send_castle(self):
        pass
    
    def recieve_castle(self):
        pass

    def check(self):
        pass