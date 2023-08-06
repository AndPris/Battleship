import pygame
import random

BACKGROUND_COLOR = (23, 227, 193)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

EMPTY_CELL = 0
MISS_CELL = 1
SHIP_CELL = 2
CRASHED_SHIP_CELL = 3

HORIZONTAL = 0
VERTICAL = 1

SAME_CELL_VALUE = 0
MISS_VALUE = 1
HIT_VALUE = 2

MISS_RADIUS = 5


class Grid:
    def __init__(self, grid_size, title):
        self.__size = grid_size
        self.__title = title
        self.__cells = [[0]*10 for i in range(self.__size)]

        self.__ships = []
        self.__cell_size = None
        self.__margin = None
        self.__left_margin = None
        self.__top_margin = None
        self.__width = None

    def display(self, screen, cell_size, margin, left_margin, top_margin, miss_radius, show_ships = False):
        self.__cell_size = cell_size
        self.__margin = margin
        self.__left_margin = left_margin
        self.__top_margin = top_margin
        self.__width = self.__size*self.__cell_size + (self.__size-1)*self.__margin

        font = pygame.font.SysFont("arial", cell_size + margin)

        title_text = font.render(self.__title, True, BLACK)
        title_text_rect = title_text.get_rect()
        title_text_rect.centerx = (left_margin*2 + (self.__size+1)*(cell_size+margin))//2
        title_text_rect.bottom = top_margin - cell_size
        screen.blit(title_text, title_text_rect)

        for row in range(self.__size):
            char = font.render(chr(row + 65), False, BLACK)
            num = font.render(str(row + 1), False, BLACK)

            char_rect = char.get_rect()
            num_rect = num.get_rect()
            char_rect.top = title_text_rect.bottom
            char_rect.centerx = left_margin + row * (margin + cell_size) + cell_size//2
            num_rect.top = top_margin + row * (margin + cell_size)
            num_rect.right = left_margin

            screen.blit(char, char_rect)
            screen.blit(num, num_rect)

        for row in range(self.__size):
            for col in range(self.__size):
                x = left_margin + (row + 1) * margin + row * cell_size
                y = top_margin + col * (margin + cell_size)
                pygame.draw.rect(screen, WHITE, (x, y, cell_size, cell_size))

                if self.__cells[col][row] == MISS_CELL:
                    pygame.draw.circle(screen, BLACK, [x + cell_size // 2, y + cell_size // 2], miss_radius, 0)
                elif self.__cells[col][row] == CRASHED_SHIP_CELL:
                    pygame.draw.line(screen, RED, (x + 3, y + 3), (x + cell_size - 3, y + cell_size - 3), 3)
                    pygame.draw.line(screen, RED, (x + cell_size - 3, y + 3), (x + 3, y + cell_size - 3), 3)
                elif show_ships and self.__cells[col][row] == SHIP_CELL:
                    pygame.draw.rect(screen, BLUE, (x, y, cell_size+margin, cell_size))

    def is_valid_start_position(self, row, col, ship_size, orientation):
        if orientation == HORIZONTAL:  # horizontal
            if col > self.__size - ship_size:
                return False

            for i in range(row - 1, row + 2):
                if i < 0 or i > self.__size-1:
                    continue
                for j in range(col - 1, col + ship_size + 1):
                    if j < 0 or j > self.__size-1:
                        continue
                    if self.__cells[i][j] == SHIP_CELL:
                        return False
        else:  # vertical
            if row > self.__size - ship_size:
                return False

            for i in range(row - 1, row + ship_size + 1):
                if i < 0 or i > self.__size-1:
                    continue
                for j in range(col - 1, col + 2):
                    if j < 0 or j > self.__size-1:
                        continue
                    if self.__cells[i][j] == SHIP_CELL:
                        return False
        return True

    def place_ship(self, ship_row, ship_col, ship_size, ship_orientation):
        self.__cells[ship_row][ship_col] = SHIP_CELL

        if ship_orientation == HORIZONTAL:
            for j in range(ship_size - 1):
                self.__cells[ship_row][ship_col + j + 1] = SHIP_CELL
        else:
            for j in range(ship_size - 1):
                self.__cells[ship_row + j + 1][ship_col] = SHIP_CELL

    def randomly_place_ships(self, ship_sizes):
        for size in ship_sizes:
            while True:
                ship_orientation = random.choice([HORIZONTAL, VERTICAL])
                if ship_orientation == HORIZONTAL:  # horizontal
                    ship_col = random.randint(0, 10 - size)
                    ship_row = random.randint(0, 9)
                else:
                    ship_col = random.randint(0, 9)
                    ship_row = random.randint(0, 10 - size)

                if self.is_valid_start_position(ship_row, ship_col, size, ship_orientation):
                    break

            self.place_ship(ship_row, ship_col, size, ship_orientation)

    def get_cell_value(self, row, col):
        return self.__cells[row][col]

    def set_cell_value(self, row, col, value):
        if row >= 0 and row <= self.__size-1 and col >= 0 and col <= self.__size-1:
            self.__cells[row][col] = value

    def shoot(self, row, col):
        if self.__cells[row][col] == MISS_CELL or self.__cells[row][col] == CRASHED_SHIP_CELL:
            return SAME_CELL_VALUE, None  # cell is already shot

        if self.__cells[row][col] == EMPTY_CELL:
            self.__cells[row][col] = MISS_CELL
            return MISS_VALUE, None  # miss

        def is_killed(row, col):
            ship_cells = [(row, col)]

            temp_row = row - 1
            while temp_row >= 0 and self.__cells[temp_row][col] != 0 and self.__cells[temp_row][col] != 1:
                ship_cells.append((temp_row, col))
                temp_row -= 1

            temp_row = row + 1
            while temp_row <= self.__size-1 and self.__cells[temp_row][col] != 0 and self.__cells[temp_row][col] != 1:
                ship_cells.append((temp_row, col))
                temp_row += 1

            temp_col = col - 1
            while temp_col >= 0 and self.__cells[row][temp_col] != 0 and self.__cells[row][temp_col] != 1:
                ship_cells.append((row, temp_col))
                temp_col -= 1

            temp_col = col + 1
            while temp_col <= self.__size-1 and self.__cells[row][temp_col] != 0 and self.__cells[row][temp_col] != 1:
                ship_cells.append((row, temp_col))
                temp_col += 1

            for cell in ship_cells:
                if self.__cells[cell[0]][cell[1]] == SHIP_CELL:
                    return False

            if len(ship_cells) == 1 or ship_cells[0][0] == ship_cells[1][0]:  # horizontal
                ship_begin_col = self.__size-1
                for cell in ship_cells:
                    if cell[1] < ship_begin_col:
                        ship_begin_col = cell[1]

                for i in range(row - 1, row + 2):
                    if i < 0 or i > self.__size-1:
                        continue
                    for j in range(ship_begin_col - 1, ship_begin_col + len(ship_cells) + 1):
                        if j < 0 or j > self.__size-1:
                            continue

                        if self.__cells[i][j] == EMPTY_CELL:
                            self.__cells[i][j] = MISS_CELL
            else:  # vertical
                ship_begin_row = self.__size-1
                for cell in ship_cells:
                    if cell[0] < ship_begin_row:
                        ship_begin_row = cell[0]

                for i in range(ship_begin_row - 1, ship_begin_row + len(ship_cells) + 1):
                    if i < 0 or i > self.__size-1:
                        continue
                    for j in range(col - 1, col + 2):
                        if j < 0 or j > self.__size-1:
                            continue

                        if self.__cells[i][j] == EMPTY_CELL:
                            self.__cells[i][j] = MISS_CELL
            return True

        self.__cells[row][col] = CRASHED_SHIP_CELL
        if row - 1 >= 0 and col - 1 >= 0:
            self.__cells[row - 1][col - 1] = 1
        if row - 1 >= 0 and col + 1 <= self.__size - 1:
            self.__cells[row - 1][col + 1] = 1
        if row + 1 <= self.__size - 1 and col + 1 <= self.__size - 1:
            self.__cells[row + 1][col + 1] = 1
        if row + 1 <= self.__size - 1 and col - 1 >= 0:
            self.__cells[row + 1][col - 1] = 1

        return HIT_VALUE, is_killed(row, col)  # hit

    def is_loose(self):
        crashed_cells = 0

        for i in range(self.__size):
            for j in range(self.__size):
                if self.__cells[i][j] == CRASHED_SHIP_CELL:
                    crashed_cells += 1
        return crashed_cells == 20

    def top(self):
        return self.__top_margin

    def bottom(self):
        return self.__top_margin + self.__width

    def left(self):
        return self.__left_margin

    def right(self):
        return self.__left_margin + self.__width

    def belongs(self, x, y):
        if x < self.left():
            return False
        if x > self.right():
            return False
        if y < self.top():
            return False
        if y > self.bottom():
            return False
        return True

    def get_coords(self, x, y):
        if not self.belongs(x, y):
            return [None, None]

        row = (y-self.__top_margin) // (self.__cell_size+self.__margin)
        col = (x-self.__left_margin) // (self.__cell_size+self.__margin)
        return [row, col]

    def get_precise_coords(self, x, y):
        if not self.belongs(x, y):
            return [None, None]

        row, col = self.get_coords(x, y)

        precise_x = self.__left_margin + col * (self.__cell_size + self.__margin)
        precise_y = self.__top_margin + row * (self.__cell_size + self.__margin)

        return [precise_x, precise_y]

    def is_ships_placed(self):
        counted_ship_cells = 0

        for i in range(self.__size):
            for j in range(self.__size):
                if self.__cells[i][j] == SHIP_CELL:
                    counted_ship_cells += 1

        return counted_ship_cells == 20
