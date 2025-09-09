import pygame
from pygame import mixer
import random
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BALL_BASE_SPEED

class Ball:
    mixer.init()
    mixer.music.load("C:/Users/ermiy/Downloads/Pong-sound.MP3")
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = None
        self.base_speed = BALL_BASE_SPEED

        #bounding box for the ball...for colliison detection
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def starting_direction(self):
        direction = ("right", "left")
        self.direction = random.choice(direction)

        # ball starting direction based on the loser
        if self.rect.left < 0:
            self.direction = direction[1]
        elif self.rect.right > WINDOW_WIDTH:
            self.direction = direction[0]

        # ball starting direction with proper speed and slight vertical movement
        if self.direction == "right":
            self.speed_x = self.base_speed
        else:
            self.speed_x = -self.base_speed
        
        # Add slight random vertical movement to make game more interesting
        self.speed_y = random.uniform(-2, 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Top and bottom walls (bounce)
        if self.y <= self.radius:
            self.speed_y = abs(self.speed_y)  # Bounce down
            self.y = self.radius
            mixer.music.play()
        elif self.y + self.radius >= WINDOW_HEIGHT:
            self.speed_y = -abs(self.speed_y)  # Bounce up
            self.y = WINDOW_HEIGHT - self.radius
            mixer.music.play()

        # Keep the rect in sync with the circle's center for collision checks
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))

    def reset_ball(self):
        """Reset ball to center with random direction"""
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2
        self.starting_direction()
        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))

    def paddle_collision(self, paddle_rect, is_left_paddle):
        """Handle paddle collision with improved physics"""
        if is_left_paddle:
            self.x = paddle_rect.right + self.radius
            self.speed_x *= -1
            self.speed_x += 0.5 if self.speed_x > 0 else -0.5
        else:
            self.x = paddle_rect.left - self.radius
            self.speed_x *= -1
            self.speed_x += -0.5 if self.speed_x < 0 else 0.5


        # Calculate deflection angle based on where ball hits paddle
        paddle_center = paddle_rect.centery
        ball_center = self.y
        relative_intersect = (paddle_center - ball_center) / (paddle_rect.height / 2)

        # Deflect ball based on hit position (more realistic physics)
        self.speed_y = -relative_intersect * self.base_speed * 0.9

        if abs(self.speed_y) < 1:
            self.speed_y = 1 if self.speed_y >= 0 else -1

        self.rect.topleft = (int(self.x - self.radius), int(self.y - self.radius))
        mixer.music.play()
