#NOTE: THE NET
# --------------

import pygame
from settings import WINDOW_HEIGHT

class Divider:
    def __init__(self, screen):
        self.screen = screen
        self.color = 'green'
        self.netWidth = 4
        self.netHeight = 15

    def draw(self, screen):
        screenRect = screen.get_rect()
        centerX = (screenRect.centerx) - (self.netWidth / 2)
        start_y = screenRect.top

        step = self.netHeight*1.6
        numOfRects = int(WINDOW_HEIGHT // step)

        for i in range(numOfRects+1):
            yCor = start_y + i*step
            net_rect = pygame.Rect(centerX, yCor, self.netWidth, self.netHeight)
            pygame.draw.rect(screen, self.color, net_rect)
