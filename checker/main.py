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
    font = pygame.font.Font("C:/Users/ermiy/Documents/robus-font/Robus-BWqOd.otf", 120)
    textColor = "White"
    textSurface = font.render("Checkers", True, textColor)
    textRect = textSurface.get_rect()
    textX = (WIDTH / 7) - textRect.width/2

    board = Board(WINDOW, BOARD_WIDTH, BOARD_HEIGHT)
    borderStartX = (WIDTH - BOARD_WIDTH) // 2
    borderStartY = (HEIGHT - BOARD_HEIGHT) // 2

    # IMAGES USED 
    startImg = pygame.image.load("C:/Users/ermiy/Downloads/Button (3).png").convert_alpha()
    exitImg = pygame.image.load("C:/Users/ermiy/Downloads/Button (2).png").convert_alpha()
    scoreImg = pygame.image.load("C:/Users/ermiy/Downloads/ScorePanel.png").convert_alpha()
    scorePanel = pygame.transform.scale(scoreImg, (int(scoreImg.get_width()*0.17), int(scoreImg.get_height()*0.2)))
    print(startImg.get_width())

    startBtn = Button(WINDOW, 1065,200, startImg, 0.14)
    exitBtn = Button(WINDOW, 1065,270, exitImg, 0.14)
    arr = [startBtn, exitBtn]

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
        WINDOW.blit(textSurface, (textX,150))
        WINDOW.blit(scorePanel, ((borderStartX+35 - scorePanel.get_width())/2, 280))

        for btn in arr:
            btn.draw()

        board.draw_board()
        pygame.draw.rect(WINDOW, "#364153", (borderStartX +40,borderStartY - 30, BOARD_WIDTH + 60, BOARD_HEIGHT + 60), width=2, border_radius=10)
        pygame.display.update()


if __name__ == "__main__":
    run_game()
