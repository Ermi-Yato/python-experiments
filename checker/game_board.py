# GAME BOARD
import pygame
from settings import BOARD_HEIGHT, BOARD_WIDTH, HEIGHT, ROWS, COLS, CELL_SIZE, WIDTH
from settings import BLACK, WHITE, BLACK_PIECE_COLOR, WHITE_PIECE_COLOR
from pieces import Pieces
from game_functions import isKingPiece, onClick, move_piece, get_all_capture_moves, get_capture_moves

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
                if (row+col) % 2 != 0:
                    if row < 3:
                        self.piecesArray[row].append(Pieces(BLACK_PIECE_COLOR, row, col, self.window, False))
                    elif row > 4:
                        self.piecesArray[row].append(Pieces(WHITE_PIECE_COLOR, row, col, self.window, False))
                    else:
                        self.piecesArray[row].append(None)
                else:
                    self.piecesArray[row].append(None)

    def draw_board(self):
        startX = (WIDTH - BOARD_WIDTH) / 2
        startY = (HEIGHT - BOARD_HEIGHT) / 2
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row+col)%2 == 0 else BLACK
                pygame.draw.rect(self.window, color, (startX + col*CELL_SIZE, startY + row*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.piecesArray[row][col]
                if piece is not None:
                    piece.draw_piece()

    def handle_click(self, mouseX, mouseY):
        row, col = onClick(mouseX, mouseY)
        clicked_piece = self.piecesArray[row][col]
        all_captures = get_all_capture_moves(self.piecesArray, self.turn)

        if self.allowed_captures:
            if [row,col] not in self.allowed_captures:
                print("You must finish capturing first")
                return

        if self.selected_piece is None:
            if len(all_captures) > 0:
                for obj in all_captures:
                    if obj["piece"] == clicked_piece:
                        self.selected_piece = clicked_piece
                        return
                print("You have to capture!")
                return

            if clicked_piece is not None and clicked_piece.color == self.turn:
                self.selected_piece = clicked_piece
                return

        else:
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
                isMoved = move_piece(self.selected_piece, row, col, self.piecesArray)
                if isMoved == "normal":
                    isKingPiece(self.piecesArray)
                    self.selected_piece = None
                    self.turn = BLACK_PIECE_COLOR if self.turn == WHITE_PIECE_COLOR else WHITE_PIECE_COLOR
                    return

                if isMoved == "capture":
                    isKingPiece(self.piecesArray)
                    nextCapPos = get_capture_moves(self.selected_piece, self.piecesArray)

                    if nextCapPos:
                        self.allowed_captures = nextCapPos[0]
                        self.selected_piece = self.selected_piece
                    else:
                        self.selected_piece = None
                        self.allowed_captures = []
                        self.turn = BLACK_PIECE_COLOR if self.turn == WHITE_PIECE_COLOR else WHITE_PIECE_COLOR
