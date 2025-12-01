#================
# PIECES CLASS
# ===============
import pygame
from settings import BLACK_PIECE_COLOR, BOARD_HEIGHT, BOARD_WIDTH, CELL_SIZE, HEIGHT, WHITE_PIECE_COLOR, WIDTH

class Pieces():
    def __init__(self, color, row, col, window, isKing=False):
        self.color = color
        self.row = row
        self.col = col
        self.window = window
        self.isKing = isKing

    def draw_piece(self):
        startX = (WIDTH - BOARD_WIDTH) / 2
        startY = (HEIGHT - BOARD_HEIGHT) / 2
        center_x = startX+70 + (self.col * CELL_SIZE + CELL_SIZE // 2)
        center_y = startY + (self.row * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(self.window, self.color, (center_x, center_y), 30)
        if self.color == WHITE_PIECE_COLOR:
            c = "#FAF9F6"
        if self.color == BLACK_PIECE_COLOR:
            c = "black"
        pygame.draw.circle(self.window, c, (center_x, center_y), 25)

        if self.isKing:
            pygame.draw.circle(self.window, "red", (center_x, center_y), 20) 
            pygame.draw.circle(self.window, "red", (center_x, center_y), 10)
