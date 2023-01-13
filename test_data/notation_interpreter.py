import re
from constants import *


"""
    Change chess notation in files to game-accessible format
"""

class NotationInterpreter:
    def __init__(self):
        self.letter_to_piece = {'r':ROOK,'n':KNIGHT,'b':BISHOP,'q':QUEEN,'k':KING}
        self.letter_to_number = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8}

    def get_team_from_turn(self, turn):
        if turn % 2 == 0:
            return WHITE
        else:
            return BLACK

    def get_piece_type(self, move):
        if self.get_is_king_side_castle(move) or self.get_is_queen_side_castle(move):
            return KING

        if move[0].isupper():
            return self.letter_to_piece[move[0].lower()]
        else:
            return PAWN

    def get_piece_indicator(self, move):
        row = None          # returning None signals there is no ambiguity/only one piece of type can do move
        column = None
        lower_case_letters = re.findall('[a-z]',move)  
        if len(lower_case_letters) > 1:
            
            if lower_case_letters[0] == 'x':
                row = self.letter_to_number[lower_case_letters[1]] # if there is a column/row indicator, it comes before the to_square
            else:
                row = self.letter_to_number[lower_case_letters[0]]

        numbers = re.findall('[0-9]',move)
        if len(numbers) > 1:
            column = numbers[0]
            
        return (row, column)

    def get_to_square(self, move):
        row = None
        column = None
        
        if self.get_is_king_side_castle(move) or self.get_is_queen_side_castle(move):
            return (row, column)

        row_column = re.findall('[a-z][0-9]',move)[-1]  # always will be the last lowercase-followed-by-number, except for castles
        row = self.letter_to_number[row_column[0]]
        column = row_column[1]
        
        return (row, column)
            

    def get_is_take(self, move):
        if 'x' in move:
            return True
        return False

    def get_is_check(self, move):
        if '+' in move:
            return True
        return False

    def get_is_checkmate(self, move):
        if '#' in move:
            return True
        return False

    def get_is_promotion(self, move):
        if '=' in move:
            return True
        return False

    def get_is_king_side_castle(self, move):
        if 'O-O' in move and not self.get_is_queen_side_castle(move): # uggo but gets the job done
            return True
        return False

    def get_is_queen_side_castle(self, move):
        if 'O-O-O' in move:
            return True
        return False

    def get_data_from_move(self, move):
        piece_type = self.get_piece_type(move)
        piece_indicator = self.get_piece_indicator(move)
        to_square = self.get_to_square(move)
        is_take = self.get_is_take(move)
        is_check = self.get_is_check(move)
        is_checkmate = self.get_is_checkmate(move)
        is_promotion = self.get_is_promotion(move)
        is_king_side_castle = self.get_is_king_side_castle(move)
        is_queen_side_castle = self.get_is_queen_side_castle(move)
        
        return {
                'piece_type':        piece_type, 
                'piece_indicator': piece_indicator, 
                'to_square':    to_square, 
                'is_take':      is_take, 
                'is_check':     is_check, 
                'is_checkmate': is_checkmate, 
                'is_promotion': is_promotion,
                'is_king_side_castle':is_king_side_castle,
                'is_queen_side_castle':is_queen_side_castle
                }

    def parse_move(self, move, turn):
        move_data = self.get_data_from_move(move)
        team = self.get_team_from_turn(turn)

        # is_king = move_data['piece_type'] == KING
        # is_pawn = move_data['piece_type'] == PAWN

        # TODO: determine if this is too tightly coupled. I think it would be...
        # if not is_king and not is_pawn:
        #     move_type = STANDARD_MOVE
        # elif is_king:
        #     if move_data['is_king_side_castle'] or move_data['is_queen_side_castle']:
        #         move_type = CASTLING
        #     else:
        #         move_type = KING_MOVE
        # elif is_pawn:
        #     if move_data['is_take']:
        #         move_type = PAWN_ATTACK
        #     elif move_data['is_take']
        
        move_data['turn'] = turn
        move_data['team'] = team

        return move_data