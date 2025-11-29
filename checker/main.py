import pygame
from settings import BOARD_HEIGHT, BOARD_WIDTH, WIDTH, HEIGHT
from game_board import Board

def run_game():
    pygame.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")

    # try to display a text
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 50)
    textColor = "gray"
    textSurface = font.render("Checkers", True, textColor)

    board = Board(WINDOW, BOARD_WIDTH, BOARD_HEIGHT)
    borderStartX = (WIDTH - BOARD_WIDTH) // 2
    borderStartY = (HEIGHT - BOARD_HEIGHT) // 2

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
        WINDOW.blit(textSurface, (0,0))
        board.draw_board()
        pygame.draw.rect(WINDOW, "#364153", (borderStartX - 30,borderStartY - 30, BOARD_WIDTH + 60, BOARD_HEIGHT + 60), width=2, border_radius=10)
        pygame.display.update()


if __name__ == "__main__":
    run_game()
