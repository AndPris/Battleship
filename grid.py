import pygame
import random

BACKGROUND_COLOR = (23, 227, 193)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

EMPTY_CELL = 0
MISS_CELL = 1
SHIP_CELL = 2
CRASHED_SHIP_CELL = 3


class Grid:
    def __init__(self, grid_size, title):
        self.__size = grid_size
        self.__title = title
        self.__cells = [[EMPTY_CELL]*10 for i in range(self.__size)]

    def display(self, screen, cell_size, margin, right_margin, top_margin, miss_radius, show_ships):
        font = pygame.font.SysFont("arial", cell_size + margin)

        title_text = font.render(self.__title, True, BLACK)
        title_text_rect = title_text.get_rect()
        title_text_rect.center = ((right_margin*2 + (self.__size+1)*(cell_size+margin))//2, top_margin//2)
        screen.blit(title_text, title_text_rect)

        for row in range(self.__size):
            char = font.render(chr(row + 65), False, BLACK)
            num = font.render(str(row + 1), False, BLACK)

            char_rect = char.get_rect()
            num_rect = num.get_rect()
            char_rect.top = top_margin
            char_rect.right = right_margin + (row + 1) * (margin + cell_size) - 7  # -7 for better align
            num_rect.top = top_margin + (row + 1) * (margin + cell_size)
            num_rect.right = right_margin

            screen.blit(char, char_rect)
            screen.blit(num, num_rect)

        for row in range(self.__size):
            for col in range(self.__size):
                x = right_margin + (row + 1) * margin + row * cell_size
                y = top_margin + (col + 1) * (margin + cell_size)
                pygame.draw.rect(screen, WHITE, (x, y, cell_size, cell_size))

                if self.__cells[col][row] == MISS_CELL:
                    pygame.draw.circle(screen, BLACK, [x + cell_size // 2, y + cell_size // 2], miss_radius, 0)
                elif self.__cells[col][row] == show_ships:
                    pygame.draw.line(screen, RED, (x + 3, y + 3), (x + cell_size - 3, y + cell_size - 3), 3)
                    pygame.draw.line(screen, RED, (x + cell_size - 3, y + 3), (x + 3, y + cell_size - 3), 3)

    def randomly_place_ships(self, ship_sizes):
        def is_valid_start_position(row, col, ship_size, orientation):
            if orientation == 0:  # horizontal
                for i in range(row - 1, row + 2):
                    if i < 0 or i > 9:
                        continue
                    for j in range(col - 1, col + ship_size + 1):
                        if j < 0 or j > 9:
                            continue
                        if self.__cells[i][j] == SHIP_CELL:
                            return False
            else:  # vertical
                for i in range(row - 1, row + ship_size + 1):
                    if i < 0 or i > 9:
                        continue
                    for j in range(col - 1, col + 2):
                        if j < 0 or j > 9:
                            continue
                        if self.__cells[i][j] == SHIP_CELL:
                            return False
            return True

        def place_ship(ship_size):
            ship_orientation = random.randint(0, 1)

            if ship_orientation == 0:  # horizontal
                ship_col = random.randint(0, 10 - ship_size)
                ship_row = random.randint(0, 9)
                while not is_valid_start_position(ship_row, ship_col, ship_size, ship_orientation):
                    ship_col = random.randint(0, 10 - ship_size)
                    ship_row = random.randint(0, 9)

                self.__cells[ship_row][ship_col] = SHIP_CELL

                for j in range(ship_size - 1):
                    self.__cells[ship_row][ship_col + j + 1] = SHIP_CELL
            else:  # vertical
                ship_col = random.randint(0, 9)
                ship_row = random.randint(0, 10 - ship_size)
                while not is_valid_start_position(ship_row, ship_col, ship_size, ship_orientation):
                    ship_col = random.randint(0, 9)
                    ship_row = random.randint(0, 10 - ship_size)

                self.__cells[ship_row][ship_col] = SHIP_CELL

                for j in range(ship_size - 1):
                    self.__cells[ship_row + j + 1][ship_col] = SHIP_CELL

            return True

        for size in ship_sizes:
            while not place_ship(size):
                pass
