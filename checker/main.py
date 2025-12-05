from game_functions import gameWinner, get_piece_count
import pygame
from settings import BLACK_PIECE_COLOR, BOARD_HEIGHT, BOARD_WIDTH, WHITE_PIECE_COLOR, WIDTH, HEIGHT
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

class Text():
    def __init__(self, window, fontType, caption, x, y, size, color):
        self.window = window
        self.caption = caption
        self.x = x
        self.y = y
        self.size = size

        self.fontType = pygame.font.Font(fontType, self.size)
        self.textSurface = self.fontType.render(self.caption, True, color)
        self.textRect = self.textSurface.get_rect()

    def blit(self):
        self.window.blit(self.textSurface, (self.x, self.y))

def run_game():
    pygame.init()
    pygame.font.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")

    board = Board(WINDOW, BOARD_WIDTH, BOARD_HEIGHT)
    gameTitle = Text(WINDOW, "C:/Users/ermiy/Documents/robus-font/Robus-BWqOd.otf", "Checkers", 25, 150, 120, "White")
    turnTitle = Text(WINDOW, "C:/Users/ermiy/Documents/Orbitron/Orbitron-VariableFont_wght.ttf", "CURRENT TURN", 110, 310, 20, "#99A1AF")

    borderStartX = (WIDTH - BOARD_WIDTH) // 2
    borderStartY = (HEIGHT - BOARD_HEIGHT) // 2

    # IMAGES USED
    startImg = pygame.image.load("C:/Users/ermiy/Downloads/Button (3).png").convert_alpha()
    exitImg = pygame.image.load("C:/Users/ermiy/Downloads/Button (2).png").convert_alpha()
    scoreImg = pygame.image.load("C:/Users/ermiy/Downloads/ScorePanel.png").convert_alpha()
    restartImg = pygame.image.load("C:/Users/ermiy/Downloads/Button (4).png").convert_alpha()
    scorePanel = pygame.transform.scale(scoreImg, (int(scoreImg.get_width()*0.17), int(scoreImg.get_height()*0.2)))

    startBtn = Button(WINDOW, 1065,200, startImg, 0.14)
    exitBtn = Button(WINDOW, 1065,270, exitImg, 0.14)
    restartBtn = Button(WINDOW, 0,0, restartImg, 0.14)
    arr = [startBtn, exitBtn, restartBtn]

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        winner = gameWinner(board.piecesArray)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if not winner:
                    board.handle_click(mouseX, mouseY)


        # display turn 
        if board.turn == WHITE_PIECE_COLOR:
            text = "WHITE"
        if board.turn == BLACK_PIECE_COLOR:
            text = "BLACK"
        if winner:
            text = f"{winner} WINS!"

        turn = Text(WINDOW, "C:/Users/ermiy/Documents/Orbitron/Orbitron-VariableFont_wght.ttf", text, 150, 350, 25, "white")

        whitePieces = get_piece_count(board.piecesArray, WHITE_PIECE_COLOR)
        blackPieces = get_piece_count(board.piecesArray, BLACK_PIECE_COLOR)

        wcount = Text(WINDOW, "C:/Users/ermiy/Documents/Orbitron/Orbitron-VariableFont_wght.ttf", f"WHITE PIECE --------------------- {whitePieces}", 50, 450, 15, "#99A1AF")
        bcount = Text(WINDOW, "C:/Users/ermiy/Documents/Orbitron/Orbitron-VariableFont_wght.ttf", f"BLACK PIECE --------------------- {blackPieces}", 50, 480, 15, "#99A1AF")


        WINDOW.fill("#172030")
        gameTitle.blit()
        WINDOW.blit(scorePanel, ((borderStartX+35 - scorePanel.get_width())/2, 280))
        turnTitle.blit()

        if not winner:
            wcount.blit()
            bcount.blit()

        if not winner:
            turn.blit()
        else:
            turn = Text(WINDOW, "C:/Users/ermiy/Documents/Orbitron/Orbitron-VariableFont_wght.ttf", text, 130, 360, 20, "white")
            turn.blit()

        for btn in arr:
            btn.draw()

        board.draw_board()

        if not winner:
            pygame.draw.rect(WINDOW, "#364153", (borderStartX +40,borderStartY - 30, BOARD_WIDTH + 60, BOARD_HEIGHT + 60), width=2, border_radius=10)

        pygame.display.update()


if __name__ == "__main__":
    run_game()
