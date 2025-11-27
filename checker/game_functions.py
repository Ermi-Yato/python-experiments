from settings import BLACK_PIECE_COLOR, CELL_SIZE, COLS, ROWS, WHITE_PIECE_COLOR

def onClick(mouseX, mouseY):
    row = mouseY // CELL_SIZE
    col = mouseX // CELL_SIZE
    return int(row), int(col)

def move_piece(piece, new_row, new_col, piecesArray):
    # this function returns None, or
    prevRow, prevCol = piece.row, piece.col
    rowDiff = new_row - prevRow
    colDiff = new_col - prevCol

    # ATTEMPT TO MOVE ONTO OCCUPIED SQUARE
    if piecesArray[new_row][new_col] is not None:
        return None
   
    # NORMAL MOVE
    if abs(rowDiff) == 1 and abs(colDiff) == 1:
        if piece.color == WHITE_PIECE_COLOR:
            if new_row > prevRow:
                return None
        else:
            if prevRow > new_row:
                return None

        piecesArray[prevRow][prevCol] = None
        piecesArray[new_row][new_col] = piece

        piece.row = new_row
        piece.col = new_col

        return "normal"

    # ATTEMPT TO CAPTURE
    if abs(rowDiff) == 2 and abs(colDiff) == 2:
        mid_row = (prevRow + new_row) // 2
        mid_col = (prevCol + new_col) // 2
        enemy_piece = piecesArray[mid_row][mid_col]

        if enemy_piece and enemy_piece.color != piece.color:
            piecesArray[mid_row][mid_col] = None
            piecesArray[prevRow][prevCol] = None
            piecesArray[new_row][new_col] = piece

            piece.row = new_row
            piece.col = new_col

            return "capture"

        return None

    return None

def get_all_capture_moves(piecesArray, color):
    all_possible_captures = []
    for row in range(ROWS):
        for col in range(COLS):
            piece = piecesArray[row][col]

            if piece is None or piece.color != color:
                continue

            captures = get_capture_moves(piece, piecesArray)
            for capture in captures:
                if len(capture) > 0:
                    all_possible_captures.append({
                        "piece": piece,
                        "moves": capture
                    })

    return all_possible_captures

def get_capture_moves(piece, piecesArray):
    row, col = piece.row, piece.col
    captures = []
    moveDirection = [(-1,-1), (-1,1), (1,-1), (1,1)]

    for rowDir, colDir in moveDirection:
        mid_row = row + rowDir
        mid_col = col + colDir
        landing_row = row + rowDir*2
        landing_col = col + colDir*2

        if not(0 <= mid_row < ROWS and 0 <= mid_col < COLS):
            continue
        if not(0 <= landing_row < ROWS and 0 <= landing_col < COLS):
            continue

        middle_piece = piecesArray[mid_row][mid_col]
        landing_piece = piecesArray[landing_row][landing_col]

        if middle_piece and middle_piece.color != piece.color:
            if landing_piece is None:

                # SIMULATE CAPTURE
                piecesArray[landing_row][landing_col] = piece
                piece.row, piece.col = landing_row, landing_col

                nextcaptures = get_capture_moves(piece, piecesArray)
                landingPos = [landing_row, landing_col]

                if not nextcaptures:
                    captures.append([landingPos])
                else:
                    for sequence in nextcaptures:
                        captures.append([landingPos] + sequence)

                # RESTORE
                piecesArray[landing_row][landing_col] = None
                piece.row, piece.col = row, col

    return captures

# WARNING: NEEDS A FIX
def get_normal_moves(piece, piecesArray):
    prevRow, prevCol = piece.row, piece.col
    moveDirection = [(-1,-1), (-1,1), (1,-1), (1,1)]

    for rDir, colD in moveDirection:
        new_row = prevRow + rDir
        new_col = prevCol + colD

        if not(0 <= new_row < ROWS and 0 <= new_col < COLS):
            continue
        if piecesArray[new_row][new_col] is None:
            return True
  
    return False

def get_legal_moves(piecesArray, color):
    for row in range(ROWS):
        for col in range(COLS):
            piece = piecesArray[row][col]

            if piece is None or piece.color != color:
                continue

            if get_normal_moves(piece, piecesArray):
                return True
            if get_capture_moves(piece, piecesArray):
                return True

    return False

def gameWinner(piecesArray):
    whitePieces = get_piece_count(piecesArray, WHITE_PIECE_COLOR)
    blackPieces = get_piece_count(piecesArray, BLACK_PIECE_COLOR)

    # 1st case
    if whitePieces == 0:
        return "BLACK"
    if blackPieces == 0:
        return "WHITE"
    
    if not get_legal_moves(piecesArray, WHITE_PIECE_COLOR):
        return "BLACK"
    if not get_legal_moves(piecesArray, BLACK_PIECE_COLOR):
        return "WHITE"

    return None

# get piece count with turn
def get_piece_count(piecesArray, turnColor):
    pieces = []
    for row in range(ROWS):
        for col in range(COLS):
            piece = piecesArray[row][col]

            if piece is None:
                continue
            if piece.color != turnColor:
                continue

            pieces.append(piece)

    return len(pieces)

