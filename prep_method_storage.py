def parse_game_notes(notation):
    inputs = []
    expected_results = []
    for turn, move_notation in enumerate(notation.split()):  # notation is algebraic chess notation with each move separated by space
        current_board = get_board(inputs)   # build board off of all previous boards

        # goal of unit test will be to find if the move from game is possible on that board according to my code
        start_position, end_position, piece_type, move_type, causes_check, ends_game, ends_how = parse_move(current_board, move_notation)
        
        current_board_fen = current_board.to_fen()

        inputs.append(
            {
                'current_board_fen': current_board_fen, # stored as FEN string
                'turn':turn,
                'piece_type':piece_type,
                'start_position':start_position,
                'end_position':end_position,
            }
        )
        expected_results.append(
            {
                'move_type':move_type,
                'causes_check':causes_check,
                'ends_game':ends_game,
                'ends_how': ends_how
            }
        )
            if ends_game:
                break
    
    return inputs, expected_results


# reuses already parsed turns
def get_board(past_inputs):
    if past_inputs:
        new_board = notation_move(past_inputs[-1])
        return Board( new_board )
    else:
        return Board()

def parse_move(current_board, move):
    start_position = get_start_position(current_board, move)
    end_position = get_end_position(current_board, move)
    piece_type = get_piece_type(move)
    move_type = get_move_type(current_board, move)
    causes_check = results_in_check(move)
    ends_game = ends_game(move)
    ends_how = ends_how(move)

    return start_position, end_position, piece_type, move_type, causes_check, ends_game, ends_how

def results_in_check(move):
    if '+' in move:
        return True
    return False


def get_start_position(current_board, move):
    pass

def get_end_position(current_board, move):
    pass

piece_notation_to_piece_type = {'r': ROOK, 'n': KNIGHT, 'b':BISHOP, 'q':QUEEN, 'k':KING}
def get_piece_type(move):
    if move[0].isupper():
        return piece_notation_to_piece_type[move[0].lower()]
    else:
        return PAWN

# WARNING !!!! heavily dependent on how I set up my move interface
def get_move_type(current_board, move):
    piece_type = get_piece_type(move)
    if piece_type in [ROOK, KNIGHT, BISHOP, QUEEN]:
        return STANDARD_MOVE
    
    if piece_type == KING:
        if 'o' in move.lower():
            return CASTLING
        else:
            return KING_MOVE

    if piece_type == PAWN:
        # if move[-1].isupper():  # example: e8Q, or e8=Q
        #     return PROMOTION
        if 'x' in move.lower():
            return PAWN_ATTACK
        letter_to_col_num = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}

        # pawn moves written like a7 or b3
        column = letter_to_col_num[move[0]]
        row = move[1]
        
        return False
    
def ends_game(move):
    pass


def ends_how(move):
    pass
    
def game_note_loader(path = 'games.txt'):
    with open(path, 'r') as file:
        for game_notes in file.readlines():
            yield game_notes

from tqdm import tqdm
def get_test_data():
    # track which move types succeed vs fail

    for game_notes in tqdm(game_note_loader()):
        inputs, expected_outputs = parse_game_notes(game_notes)

        

if __name__ == '__main__':
    get_test_data()