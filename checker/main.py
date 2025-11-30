import pygame
from settings import BOARD_HEIGHT, BOARD_WIDTH, WIDTH, HEIGHT
from game_board import Board

class Button():
    def __init__(self, screen, xCor, yCor, image, scale):
        self.screen = screen
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)) )
        self.rect = self.image.get_rect()
        self.rect.topleft = (xCor, yCor)

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))


def run_game():
    pygame.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")

    # try to display a text
    pygame.font.init()
    # font = pygame.font.SysFont("Arial", 50)
    font = pygame.font.Font("C:/Users/ermiy/Documents/robus-font/Robus-BWqOd.otf", 80)
    textColor = "White"
    textSurface = font.render("Checkers", True, textColor)
    textRect = textSurface.get_rect()
    textX = (WIDTH / 2) - textRect.width/2

    board = Board(WINDOW, BOARD_WIDTH, BOARD_HEIGHT)
    borderStartX = (WIDTH - BOARD_WIDTH) // 2
    borderStartY = (HEIGHT - BOARD_HEIGHT) // 2

    startBtn = pygame.image.load("C:/Users/ermiy/Downloads/Button (3).png").convert_alpha()
    exitBtn = pygame.image.load("C:/Users/ermiy/Downloads/Button (2).png").convert_alpha()
    button1 = Button(WINDOW, WIDTH - 250,40, startBtn, 0.16)
    button2 = Button(WINDOW, WIDTH - 250,150, exitBtn, 0.16)
    arr = [button1,button2]

    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                board.handle_click(mouseX, mouseY)

        WINDOW.fill("#172030")
        WINDOW.blit(textSurface, (textX,0))

        for btn in arr:
            btn.draw()

        board.draw_board()
        pygame.draw.rect(WINDOW, "#364153", (borderStartX - 30,borderStartY - 30, BOARD_WIDTH + 60, BOARD_HEIGHT + 60), width=2, border_radius=10)
        pygame.display.update()


if __name__ == "__main__":
    run_game()
