from settings import CELL_SIZE

def onClick(mouseX, mouseY):
    row = mouseY // CELL_SIZE
    col = mouseX // CELL_SIZE
    return int(row), int(col)
