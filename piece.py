from keys import *

class Piece:
    def __init__(self, team, position):
        self.team = team
        self.position = position
        self.has_moved = False
        self.moved_last = False

        self.possible_moves = []

    def add_possible_move(self, move):
        self.possible_moves.append(move)

    def get_directions(self):   # possible moves described in x,y coords from perspective of piece going from bottom row to middle
        return self.directions

    def get_scalars(self):
        return self.scalars

    def get_team(self):
        return self.team

    def move(self):
        self.has_moved = True
        self.moved_last = True

class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.directions = [(0,1),(1,1),(-1,1)]
        self.scalars    = [1]
        self.specialset = [(self.send_enpassant, self.recieve_enpassant), 
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
        self.directions = [(1,0),(-1,0),(0,1),(0,-1)]
        self.scalars    = [    i for i in range(BOARD_ROWS)   ]
        self.specialset = []

class Knight(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.directions = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        self.scalars    = [1]
        self.specialset = []

class Bishop(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.directions = [(1,1),(1,-1),(-1,-1),(-1,1)]
        self.scalars    = [    i for i in range(BOARD_ROWS)   ]
        self.specialset = []

class Queen(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.directions = [(1,1),(1,-1),(-1,-1),(-1,1),(1,0),(-1,0),(0,1),(0,-1)]
        self.scalars    = [    i for i in range(BOARD_ROWS)   ]
        self.specialset = []

class King(Piece):
    def __init__(self, team):
        super().__init__(team)
        self.directions = [(1,1),(1,-1),(-1,-1),(-1,1),(1,0),(-1,0),(0,1),(0,-1)]
        self.scalars    = [1]
        self.specialset = [(self.send_castle, self.recieve_castle)]

    def send_castle(self):
        pass
    
    def recieve_castle(self):
        pass

    def check(self):
        pass