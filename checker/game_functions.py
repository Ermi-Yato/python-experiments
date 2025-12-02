from settings import BLACK_PIECE_COLOR, BOARD_HEIGHT, BOARD_WIDTH, CELL_SIZE, COLS, HEIGHT, ROWS, WHITE_PIECE_COLOR, WIDTH

def onClick(mouseX, mouseY):
    startX = (WIDTH - BOARD_WIDTH) / 2
    startY = (HEIGHT - BOARD_HEIGHT) / 2

    # Subtract startX and startY from the mouseX and mouseY
    row = (mouseY - startY) // CELL_SIZE
    col = (mouseX - startX-70) // CELL_SIZE
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
        if piece.color == WHITE_PIECE_COLOR and piece.isKing == False:
            if new_row > prevRow:
                return None
        if piece.color == BLACK_PIECE_COLOR and piece.isKing == False:
            if prevRow > new_row:
                return None

        piecesArray[prevRow][prevCol] = None
        piecesArray[new_row][new_col] = piece

        piece.row = new_row
        piece.col = new_col

        return "normal"

    #TODO: Implement long jump for king pieces

    # if piece.isKing:
    #     if abs(rowDiff) != 0 and abs(rowDiff) == abs(colDiff):
    #         piecesArray[prevRow][prevCol] = None
    #         piecesArray[new_row][new_col] = piece
    #
    #         piece.row = new_row
    #         piece.col = new_col
    #
    #         return "normal"
    #
    # if piece.isKing:
    #     pass
    #

    # ATTEMPT TO CAPTURE
    if abs(rowDiff) == 2 and abs(colDiff) == 2:
        mid_row = (prevRow + new_row) // 2
        mid_col = (prevCol + new_col) // 2
        enemy_piece = piecesArray[mid_row][mid_col]

        if enemy_piece and enemy_piece.color != piece.color:
            if piece.color == WHITE_PIECE_COLOR and piece.isKing == False:
                if new_row > prevRow:
                    return None
            if piece.color == BLACK_PIECE_COLOR and piece.isKing == False:
                if new_row < prevRow:
                    return None

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

    if whitePieces == 11:
        return "BLACK"
    if blackPieces == 11:
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

# detect king piece
def isKingPiece(piecesArray):
    for row in range(ROWS):
        for col in range(COLS):
            piece = piecesArray[row][col]

            if piece is None:
                continue
            result = kingDetection(piece)
            if result:
                piece.isKing = True
            else:
                piece.isKing = piece.isKing

def kingDetection(piece):
    if piece.color == WHITE_PIECE_COLOR:
        if piece.row == 0:
            return True
    if piece.color == BLACK_PIECE_COLOR:
        if piece.row == 7:
            return True

    return False



