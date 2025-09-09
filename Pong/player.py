# NOTE: THIS FILE CONTAINS EVERYTHING ABOUT THE PADDLES OR THE LEFT AND RIGHT PLAYERS
# -------------------------------------------------------------------------------------
import pygame
from settings import PADDLE_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, color, width, height):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.width = width
        self.height = height
        self.speed_y = PADDLE_SPEED

        self.image = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.image)

    def update_player_pos(self, keys, height, position):
        if position == 'right':
            if keys[pygame.K_DOWN]:
                self.image.y += self.speed_y
            if keys[pygame.K_UP]:
                self.image.y -= self.speed_y
        if position == 'left':
            if keys[pygame.K_s]:
                self.image.y += self.speed_y
            if keys[pygame.K_w]:
                self.image.y -= self.speed_y

        # Constraints on the edges of the window
        if self.image.top < 0:
            self.image.top = 0
        if self.image.bottom > height:
            self.image.bottom = height

    def reset_position(self):
        # reset the position
        self.image.x = self.x_pos
        self.image.y = self.y_pos
