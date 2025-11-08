import pygame

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8,8
CELL_SIZE = WIDTH / COLS

BLACK = (42, 45, 56)
WHITE = (211, 218, 228)
BLACK_PIECE_COLOR = (67, 71, 74)
WHITE_PIECE_COLOR = (255,255,255)

# GAME BOARD
class Board():
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.piecesArray = []
        self.selected_piece = None
        self.turn = WHITE_PIECE_COLOR
        self.initial_board()

    def initial_board(self):
        for row in range(ROWS):
            self.piecesArray.append([])
            for col in range(COLS):
                if (row+col)%2 != 0:
                    if row < 3:
                        self.piecesArray[row].append(Pieces(BLACK_PIECE_COLOR, row, col, self.window))
                    elif row > 4:
                        self.piecesArray[row].append(Pieces(WHITE_PIECE_COLOR, row, col, self.window))
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
        return int(row), int(col)

    def handle_click(self, mouseX, mouseY):
        row, col = self.onClick(mouseX,mouseY)
        clicked_piece = self.piecesArray[row][col]

        # # if no piece is selected and the clicked cell contains a piece
        if self.selected_piece is None:
            # if clicked_piece is not none and the clicked_piece is the same as the current turn
            if clicked_piece is not None and clicked_piece.color == self.turn:
                self.selected_piece = clicked_piece
                return
        else:
            if clicked_piece is not None and clicked_piece.color == self.selected_piece.color:
                self.selected_piece = clicked_piece
                return
            if clicked_piece is None:

                isMoved = self.move_piece(self.selected_piece, row, col)
                if isMoved:
                    self.selected_piece = None
                    if self.turn == WHITE_PIECE_COLOR:
                        self.turn = BLACK_PIECE_COLOR
                    else:
                        self.turn = WHITE_PIECE_COLOR
                    return


    # method to move pieces
    def move_piece(self, piece, new_row, new_col):
        # move to another filled cell
        if (self.piecesArray[new_row][new_col]) is not None:
            return False

        # get old row and col from the clicked_piece
        prevRow = piece.row
        prevCol = piece.col

        #move rules
        if (prevRow == new_row or prevCol == new_col):
            return False

        rowDiff = new_row - prevRow
        colDiff = new_col - prevCol

        if abs(rowDiff) == 1 and abs(colDiff) == 1:

            if piece.color == WHITE_PIECE_COLOR:
                if new_row > prevRow: return False
            else:
                if prevRow > new_row: return False


            self.piecesArray[prevRow][prevCol] = None
            self.piecesArray[new_row][new_col] = piece

            piece.row = new_row
            piece.col = new_col

            return True

        # check for potential capture
        if abs(rowDiff) == 2 and abs(colDiff) == 2:
            mid_row = (prevRow + new_row) // 2
            mid_col = (prevCol + new_col) // 2
            enemy_piece = self.piecesArray[mid_row][mid_col]

            if enemy_piece is not None and enemy_piece.color != piece.color:
                self.piecesArray[mid_row][mid_col] = None
                self.piecesArray[prevRow][prevCol] = None
                self.piecesArray[new_row][new_col] = piece

                piece.row = new_row
                piece.col = new_col

                return True

            return False

        return False



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
