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

        # if no piece is selected and the clicked cell contains a piece
        if self.selected_piece is None:
            if self.piecesArray[int(row)][int(col)] is not None:
                self.selected_piece = self.piecesArray[int(row)][int(col)]
        else:
            # the second click contains no piece

            self.move_piece(self.selected_piece, row, col)
            self.selected_piece = None

    # method to move pieces
    def move_piece(self, piece, new_row, new_col):
        # move to another filled cell
        if (self.piecesArray[int(new_row)][int(new_col)]) is not None:
            print("Can't move. target already occupied.")
            return
        # get old row and col
        prevRow = piece.row
        prevCol = piece.col
        
        #move rules
        if (prevRow == new_row or prevCol == new_col):
            print("Same row movement or same col movement.")
            return
        if abs(new_row - prevRow) != 1 and abs(new_col - prevCol) != 1:
            print("long jump not allowed")
            return
        if piece.color == "white":
            if new_row > prevRow:
                print("white piece backward movement...not allowed")
                return
        else:
            if prevRow > new_row:
                print("black piece backward movement...not allowed")
                return

        self.piecesArray[int(prevRow)][int(prevCol)] = None

        self.piecesArray[int(new_row)][int(new_col)] = piece
        piece.row = new_row
        piece.col = new_col



# PIECES CLASS
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
