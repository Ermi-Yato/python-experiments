#================
# PIECES CLASS
# ===============
import pygame
from settings import CELL_SIZE

class Pieces():
    def __init__(self, color, row, col, window):
        self.color = color
        self.row = row
        self.col = col
        self.window = window
        self.king = False

    def draw_piece(self):
        center_x = self.col * CELL_SIZE + CELL_SIZE // 2
        center_y = self.row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(self.window, self.color, (center_x, center_y), 30)


