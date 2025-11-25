# GAME BOARD
import pygame
from settings import ROWS, COLS, CELL_SIZE
from settings import BLACK, WHITE, BLACK_PIECE_COLOR, WHITE_PIECE_COLOR
from pieces import Pieces
from game_functions import onClick

class Board():
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.piecesArray = []
        self.selected_piece = None
        self.allowed_captures = []
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
        row, col = onClick(mouseX, mouseY)
        clicked_piece = self.piecesArray[row][col]

        # get all available captures
        all_captures = self.get_all_capture_moves(self.piecesArray, self.turn)
        
        # force to capture until the path fully ended
        if self.allowed_captures:
            if [row,col] not in self.allowed_captures:
                print("You must finish capturing first")
                return

        # if no piece is selected and the clicked cell contains a piece
        if self.selected_piece is None:
            if len(all_captures) > 0:
                # we must limit the selection to the piece who can capture
                for obj in all_captures:
                    if obj["piece"] == clicked_piece:
                        self.selected_piece = clicked_piece
                        return
                print("You have to capture!")
                return

            # if clicked_piece is not none and the clicked_piece is the same as the current turn and nothing to capture
            if clicked_piece is not None and clicked_piece.color == self.turn:
                self.selected_piece = clicked_piece
                return

        else:
            # selecting another similar piece
            if clicked_piece is not None and clicked_piece.color == self.selected_piece.color:
                if len(all_captures) > 0:
                    for obj in all_captures:
                        if obj["piece"] == clicked_piece:
                            self.selected_piece = clicked_piece
                            return
                    print("You have to capture!")
                    return

                self.selected_piece = clicked_piece
                return

            if clicked_piece is None:
                # attempt to capture
                isMoved = self.move_piece(self.selected_piece, row, col)
                if isMoved == "normal":
                    self.selected_piece = None
                    # switch turn
                    self.turn = BLACK_PIECE_COLOR if self.turn == WHITE_PIECE_COLOR else WHITE_PIECE_COLOR
                    return

                if isMoved == "capture":
                    nextCapPos = self.get_capture_moves(self.selected_piece)

                    if nextCapPos:
                        self.allowed_captures = nextCapPos[0]
                        self.selected_piece = self.selected_piece
                    else:
                        self.selected_piece = None
                        self.allowed_captures = []
                        # switch turn
                        self.turn = BLACK_PIECE_COLOR if self.turn == WHITE_PIECE_COLOR else WHITE_PIECE_COLOR
    



    def move_piece(self, piece, new_row, new_col):
        prevRow = piece.row
        prevCol = piece.col

        rowDiff = new_row - prevRow
        colDiff = new_col - prevCol

        # Prevent moving into occupied place
        if (self.piecesArray[new_row][new_col]) is not None:
            return None

                # REGULAR MOVE 
        if abs(rowDiff) == 1 and abs(colDiff) == 1:

            # For normal pieces, only forward move is possible
            if piece.color == WHITE_PIECE_COLOR:
                if new_row > prevRow: return None
            else:
                if prevRow > new_row: return None

            self.piecesArray[prevRow][prevCol] = None
            self.piecesArray[new_row][new_col] = piece

            piece.row = new_row
            piece.col = new_col

            return "normal"

        # CAPTURE ATTEMPT
        
        if abs(rowDiff) == 2 and abs(colDiff) == 2:

            # Get the enemy_piece or middle one
            mid_row = (prevRow + new_row) // 2
            mid_col = (prevCol + new_col) // 2
            enemy_piece = self.piecesArray[mid_row][mid_col]

            # If middle piece is enemy_piece
            if enemy_piece is not None and enemy_piece.color != piece.color:
                self.piecesArray[mid_row][mid_col] = None
                self.piecesArray[prevRow][prevCol] = None
                self.piecesArray[new_row][new_col] = piece

                piece.row = new_row
                piece.col = new_col

                return "capture"

            return None

        # Everything else fails
        return None

    def get_all_capture_moves(self, board, color):
        all_captures = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]

                if piece is None:
                    continue
                if piece.color != color:
                    continue

                captures = self.get_capture_moves(piece)
                for capture in captures:
                    if len(capture) > 0:
                        all_captures.append({
                            "piece": piece,
                            "moves": capture
                        })


        return all_captures

    # returns a coordinate of a capture
    def get_capture_moves(self, piece):
        row, col = piece.row, piece.col
        results = []

        moveDirection = [(-1,-1), (-1,1), (1,-1), (1,1)]

        for rowDir, colDir in moveDirection:
            mid_r = row + rowDir
            mid_c = col + colDir
            landing_r = row + rowDir*2
            landing_c = col + colDir*2

            # check for bounds
            if not(0 <= mid_r < ROWS and 0 <= mid_c < COLS):
                continue
            if not(0 <= landing_r < ROWS and 0 <= landing_c < COLS):
                continue

            middle_piece = self.piecesArray[mid_r][mid_c]
            landing_square = self.piecesArray[landing_r][landing_c]

            if middle_piece is not None and middle_piece.color != piece.color:
                if landing_square is None:
                    # simulate capturing
                    removed = self.piecesArray[mid_r][mid_c]
                    self.piecesArray[landing_r][landing_c] = piece
                    piece.row, piece.col = landing_r, landing_c

                    # call the function with update piece coordinates // recursion
                    nextcaptures = self.get_capture_moves(piece)
                    landingPos = [landing_r, landing_c]
                    
                    if not nextcaptures:
                        results.append([landingPos])
                    else:
                        for path in nextcaptures:
                            results.append([landingPos] + path)

                    # restore 
                    self.piecesArray[mid_r][mid_c] = removed
                    self.piecesArray[landing_r][landing_c] = None
                    piece.row, piece.col = row, col

        return results




