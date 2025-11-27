from game_functions import gameWinner
import pygame
from settings import WIDTH, HEIGHT
from game_board import Board

def run_game():
    pygame.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")

    board = Board(WINDOW, WIDTH, HEIGHT)

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

        winner = gameWinner(board.piecesArray)
        if winner:
            print(f"{winner} wins!")
            run = False

        board.draw_board()
        pygame.display.update()


if __name__ == "__main__":
    run_game()
