from constants import *
from piece import King

# player will be able to access all pieces and see all their legal moves
class Player:
    def __init__(self, team, all_pieces):
        self.team = team
        self.pieces = self._get_team_pieces(all_pieces)
        self.king = self._get_king(self.pieces)

        self.was_in_check_last_turn = False

    def init_piece_moves(self, board):
        pass

    

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