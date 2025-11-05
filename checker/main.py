import pygame

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8,8
CELL_SIZE = WIDTH / COLS

BLACK = (50, 34, 19)
WHITE = (241, 204, 164)

# GAME BOARD
class Board():
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.piecesArray = []
        self.selected_piece = None
        self.initial_board()

    def initial_board(self):
        for row in range(ROWS):
            self.piecesArray.append([])
            for col in range(COLS):
                if (row+col)%2 != 0:
                    if row < 3:
                        self.piecesArray[row].append(Pieces((67, 71, 74), row, col, self.window))
                    elif row > 4:
                        self.piecesArray[row].append(Pieces("white", row, col, self.window))
                    else:
                        self.piecesArray[row].append(None)
                else:
                    self.piecesArray[row].append(None)



    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row+col)%2 == 0 else BLACK
                pygame.draw.rect(self.window, color, (col*CELL_SIZE,row*CELL_SIZE,CELL_SIZE,CELL_SIZE))

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.piecesArray[row][col]
                if piece is not None:
                    piece.draw_piece()

    def onClick(self, mouseX,mouseY):
        row = mouseY // CELL_SIZE
        col = mouseX // CELL_SIZE
        return row, col

    def handle_click(self, mouseX, mouseY):
        row, col = self.onClick(mouseX,mouseY)
        if self.piecesArray[int(row)][int(col)] != None:
            self.selected_piece = self.piecesArray[int(row)][int(col)].color

# PIECES CLASS
class Pieces():
    def __init__(self, color, row, col, window):
        self.color = color
        self.row = row
        self.col = col
        self.window = window

    def draw_piece(self):
        center_x = self.col * CELL_SIZE + CELL_SIZE // 2
        center_y = self.row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(self.window, self.color, (center_x, center_y), 30)



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

        board.draw_board()
        pygame.display.update()


if __name__ == "__main__":
    run_game()
