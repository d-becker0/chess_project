from sys import exit

import pygame

from constants import *

class Interface:
    def __init__(self):
        pass

    def event_loop(self):
        for event in pygame.event.get():
            click = None
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = self._handle_click(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            

            # not great, need better way to give variety of info from events (maybe fine for this to go in main loop)
            return click
    
    def _handle_click(self, event):
        x,y = event.pos
        return x, y


class Display:
    def __init__(self, single_player = True):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(pygame.Color("white"))

        self.single_player = single_player
        self._draw_tiles()

    def _draw_tiles(self):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                color = self._choose_color(row, column)
                square_coords_and_dims = self._create_square_coords_and_dims(row, column)
                pygame.draw.rect(self.screen, color, square_coords_and_dims)

    def _choose_color(self, row, column):
        if (row + column) % 2 == 0:
            return DARK_SQUARE_COLOR
        else:
            return LIGHT_SQUARE_COLOR

    def _create_square_coords_and_dims(self, row, column):
        # left, top, height, width (I think thats the order lol)
        return (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

    def _piece_coords_by_square(self, row, column):
        left, top, height, width = self._create_square_coords_and_dims(row, column)
        return (left + 1/2 * SQUARE_SIZE, top - 1/2 * SQUARE_SIZE)
    
    def end_of_turn(self, board):
        self._draw_all(board)
        self._change_orientation()

    def _draw_all(self, board):
        self._draw_tiles()
        self._draw_pieces(board)
        # self._draw_overlay()

    def _draw_pieces(self, board):
        for row, column, piece in board.yield_coords_and_content():
            position_left, position_top = self._piece_coords_by_square(row,column)
            #self.screen.blit(piece.image, (position_left, position_top))


    def _change_orientation(self):
        if self.single_player:
            pygame.display.flip()

    def reset_board(self):
        pass