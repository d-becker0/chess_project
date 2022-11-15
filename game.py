from constants import *
from piece import King

class Player:
    def __init__(self, team, all_pieces):
        self.team = team
        self.pieces = self._get_team_pieces(all_pieces)
        self.king = self._get_king(self.pieces)

        self.was_in_check = False
        self.checking_pieces= []
        self.pinning_pieces = []
    
    def recalculate_all(self, board):
        for piece in self.pieces:
            piece.recalculate_moves(board)
    
    def in_check(self, board):
        king_square = board[self.king.row][self.king.column]
        for piece in king_square.reached_by_pieces:
            if piece.team != self.team:
                self.was_in_check = True
                return True
        self.was_in_check = False
        return False

    def _get_team_pieces(self, pieces):
        team_pieces = []
        for piece in pieces:
            if piece.team == self.team:
                team_pieces.append(piece)
        return team_pieces

    def _get_king(self, pieces):
        for piece in pieces:
            if isinstance(piece, King) and piece.team == self.team:
                return piece

class Game:
    def __init__(self):
        self.turn = 0
        self.past_boards = []

    def increment_turn(self):
        self.turn += 1

    def turn_to_team(self, turn):
        if turn % 2:
            return BLACK
        else: 
            return WHITE