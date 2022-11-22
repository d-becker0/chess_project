from constants import *
from game import Game, Player
from board import Board
from visual import Display, Interface

if __name__ == "__main__":
    board = Board()
    game = Game()
    display = Display()
    interface = Interface()

    white = Player(WHITE, board.pieces)
    black = Player(BLACK, board.pieces)

    display._draw_all(board)

    selection = None
    selected_coords = None
    running = True

    while running:
        
        current_team = game.turn_to_team(game.turn)
        pos = interface.event_loop()

        if pos:
            column, row = pos # why do I need to reverse these? -> x,y to y, x
            square = board.board[row][column]

            if (square.piece) and ( square.piece.team == current_team ):
                # previous selection
                if selected_coords:
                    display.unhighlight(selected_coords[0], selected_coords[1], selection, board.board)
                
                display.draw_selection(row, column, square, board.board)
                
                # New selected square
                selection = square
                selected_coords = (row, column)
            
            elif (selection) and selection.piece.row_col_in_current_moves(row, column):
                board.update(row, column, selection)
                
                game.increment_turn()
                display.end_of_turn(board)
                
                if white.in_check(board.board):
                    white.was_in_check = True
                    white.recalculate_all(board.board)
                elif white.was_in_check:
                    white.was_in_check = False
                    white.recalculate_all(board.board)
                
                # need to freeze all non-blocking moves or unfreeze after a check is blocked
                if black.in_check(board.board):
                    black.was_in_check = True
                    print("Black is checked", black.find_checking_pieces(board.board))
                    black.recalculate_all(board.board)
                elif black.was_in_check:
                    print("Black out of check")
                    black.was_in_check = False
                    black.recalculate_all(board.board)

                selection = None
                selected_coords = None