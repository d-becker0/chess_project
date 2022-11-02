from constants import *
class Player:
    def __init__(self, team, all_pieces):
        self.team = team
        self.pieces = self._get_team_pieces(all_pieces)

    def _get_team_pieces(self, pieces):
        team_pieces = []
        for piece in pieces:
            if piece.team == self.team:
                team_pieces.append(piece)
        return team_pieces

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