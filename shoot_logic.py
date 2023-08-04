from grid import *


def generate_coords(grid_size):
    row = random.randint(0, grid_size-1)
    col = random.randint(0, grid_size-1)

    return row, col


def smart_generate_coords(grid, row, col, grid_size):
    probable_ship_cells = []

    if (row - 1 >= 0 and grid.get_cell_value(row-1, col) == CRASHED_SHIP_CELL) or (row + 1 <= grid_size-1 and grid.get_cell_value(row+1, col) == CRASHED_SHIP_CELL):
        temp_row = row - 1
        while temp_row >= 0 and grid.get_cell_value(temp_row, col) == CRASHED_SHIP_CELL:
            temp_row -= 1

        if temp_row >= 0 and grid.get_cell_value(temp_row, col) != MISS_CELL:
            probable_ship_cells.append((temp_row, col))

        temp_row = row + 1
        while temp_row <= grid_size-1 and grid.get_cell_value(temp_row, col) == CRASHED_SHIP_CELL:
            temp_row += 1

        if temp_row <= grid_size-1 and grid.get_cell_value(temp_row, col) != MISS_CELL:
            probable_ship_cells.append((temp_row, col))

    elif (col - 1 >= 0 and grid.get_cell_value(row, col-1) == CRASHED_SHIP_CELL) or (col + 1 <= grid_size-1 and grid.get_cell_value(row, col+1) == CRASHED_SHIP_CELL):
        temp_col = col - 1
        while temp_col >= 0 and grid.get_cell_value(row, temp_col) == CRASHED_SHIP_CELL:
            temp_col -= 1

        if temp_col >= 0 and grid.get_cell_value(row, temp_col) != MISS_CELL:
            probable_ship_cells.append((row, temp_col))

        temp_col = col + 1
        while temp_col <= grid_size-1 and grid.get_cell_value(row, temp_col) == CRASHED_SHIP_CELL:
            temp_col += 1

        if temp_col <= grid_size-1 and grid.get_cell_value(row, temp_col) != MISS_CELL:
            probable_ship_cells.append((row, temp_col))
    else:
        if col-1 >= 0 and grid.get_cell_value(row, col-1) != MISS_CELL:
            probable_ship_cells.append((row, col-1))
        if col+1 <= grid_size-1 and grid.get_cell_value(row, col+1) != MISS_CELL:
            probable_ship_cells.append((row, col+1))
        if row-1 >= 0 and grid.get_cell_value(row-1, col) != MISS_CELL:
            probable_ship_cells.append((row-1, col))
        if row+1 <= grid_size-1 and grid.get_cell_value(row+1, col) != MISS_CELL:
            probable_ship_cells.append((row+1, col))

    choice = probable_ship_cells[random.randint(0, len(probable_ship_cells)-1)]
    return choice
