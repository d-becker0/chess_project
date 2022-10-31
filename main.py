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


    running = True
    while running:
        interface.event_loop()

        game.increment_turn()
        display.end_of_turn(board)