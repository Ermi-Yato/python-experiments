from settings import CELL_SIZE, WHITE_PIECE_COLOR

def onClick(mouseX, mouseY):
    row = mouseY // CELL_SIZE
    col = mouseX // CELL_SIZE
    return int(row), int(col)

def move_piece(piece, new_row, new_col, piecesArray):
    # this function returns None, or
    prevRow, prevCol = piece.row, piece.col
    rowDiff = new_row - prevRow
    colDiff = new_col - prevCol

    if piecesArray[new_row][new_col] is not None:
        return None
    
    if abs(rowDiff) == 1 and abs(colDiff) == 1:
        if piece.color == WHITE_PIECE_COLOR:
            if new_row > prevRow:
                return None
        else:
            if prevRow > new_row:
                return None

