from constants import *
from board import Game, Player, Board
from visual import Display, Interface

if __name__ == "__main__":
    board = Board()
    game = Game()
    display = Display()
    interface = Interface()

    white = Player(WHITE, board.pieces)
    black = Player(BLACK, board.pieces)

    display._draw_all(board)

    running = True
    while running:
        
        current_team = game.turn_to_team(game.turn)

        pos = interface.event_loop()

        selection = None

        if pos:
            row, column = pos
            piece = board.board[row][column]

            if piece.team == current_team:
                selection = piece
                selected_coords = (row, column)
            
            elif selection and (row, column) in selection.move_squares:
                selection.move(row, column)
                board.update(row, column, piece)
                
                game.increment_turn()
                print(game.turn)
                display.end_of_turn(board)