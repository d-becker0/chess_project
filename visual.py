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
        return x // SQUARE_SIZE, y // SQUARE_SIZE


class Display:
    def __init__(self, single_player = True):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.screen.fill(pygame.Color("white"))

        self.single_player = single_player
        self._draw_tiles()

    def _draw_tiles(self):
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                color = self._choose_color(row, column)
                self._draw_tile(row, column, color)

    def _draw_tile(self, row, column, color):
        square_coords_and_dims = self._create_square_coords_and_dims(row, column)
        pygame.draw.rect(self.screen, color, square_coords_and_dims)

    def _choose_color(self, row, column):
        if (row + column) % 2 == 0:
            return LIGHT_SQUARE_COLOR
        else:
            return DARK_SQUARE_COLOR

    def _create_square_coords_and_dims(self, row, column):
        # left, top, height, width (I think thats the order lol)
        return (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

    def _piece_coords_by_square(self, row, column):
        left, top, height, width = self._create_square_coords_and_dims(row, column)
        return left,top
    
    def end_of_turn(self, board):
        self._draw_all(board)
        self._change_orientation()

    def _draw_all(self, board):
        self._draw_tiles()
        self._draw_all_pieces(board)
        pygame.display.update()

    def _draw_all_pieces(self, board):
        for row, column, piece in board.yield_coords_and_piece():
            self._draw_piece(row, column, piece)

    def _draw_piece(self, row, column, piece):
        if piece and piece.image:
            position_left, position_top = self._piece_coords_by_square(row,column)
            self.screen.blit(  self._load_image(piece.image), (position_left, position_top)  )

    def draw_selection(self, row, column, selection, board):
        self._draw_tile(row, column, PRIMARY_HIGHLIGHT)
        self._draw_piece(row, column, selection.piece)

        # debug
        print(str(selection.piece),"at -- row:", row, "column:", column)
        print("Pieces blocked by 1 piece", str([move.piece for move in selection.blocked_for_pieces if move.pieces_in_between == 1]))
        # print("Piece's moves -- ", str(selection.piece.current_moves))
        # print("Piece blocked for --", str(selection.piece.blocked_moves))

        for move in selection.piece.current_moves:
            square = board[move.row][move.column]
            self._draw_tile(move.row, move.column, SECONDARY_HIGHLIGHT)
            self._draw_piece(move.row, move.column, square.piece)

        pygame.display.update()

    def unhighlight(self, row, column, unselected, board):
        self._draw_tile(row, column, self._choose_color(row, column))
        self._draw_piece(row, column, unselected.piece)

        for move in unselected.piece.current_moves:
            square = board[move.row][move.column]
            self._draw_tile(move.row, move.column, self._choose_color(move.row, move.column))
            self._draw_piece(move.row, move.column, square.piece)
        pygame.display.update()

    def _load_image(self, image_path):
        return pygame.image.load(image_path)

    def _change_orientation(self):
        if self.single_player == False:
            pygame.display.flip()