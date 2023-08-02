import pygame
import random
import copy

pygame.init()

BACKGROUND_COLOR = (23, 227, 193)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_SIZE = (1000, 500)
GRID_SIZE = 10
CELL_SIZE = 30
MARGIN = 1
MISS_RADIUS = 5
GRID_WIDTH = 11 * (CELL_SIZE + MARGIN)
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN = (50, 100)
COMPUTER_GRID_RIGHT_MARGIN, COMPUTER_GRID_TOP_MARGIN = (PLAYER_GRID_RIGHT_MARGIN + GRID_WIDTH + 100, PLAYER_GRID_TOP_MARGIN)


player_grid = [[0]*10 for i in range(10)]
computer_grid = [[0]*10 for i in range(10)]

font = pygame.font.SysFont("arial", CELL_SIZE + MARGIN)


def display_grid(grid, right_margin, top_margin):
    for row in range(GRID_SIZE):
        char = font.render(chr(row + 65), False, BLACK)
        num = font.render(str(row + 1), False, BLACK)

        char_rect = char.get_rect()
        num_rect = num.get_rect()
        char_rect.top = top_margin
        char_rect.right = right_margin + (row + 1) * (MARGIN + CELL_SIZE) - 7  # -7 for better align
        num_rect.top = top_margin + (row + 1) * (MARGIN + CELL_SIZE)
        num_rect.right = right_margin

        screen.blit(char, char_rect)
        screen.blit(num, num_rect)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = right_margin + (row + 1) * MARGIN + row * CELL_SIZE
            y = top_margin + (col + 1) * (MARGIN + CELL_SIZE)
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

            if grid[col][row] == 1:
                pygame.draw.circle(screen, BLACK, [x + CELL_SIZE//2, y + CELL_SIZE//2], MISS_RADIUS, 0)
            elif grid[col][row] == 3:
                pygame.draw.line(screen, RED, (x+3, y+3), (x+CELL_SIZE-3, y+CELL_SIZE-3), 3)
                pygame.draw.line(screen, RED, (x+CELL_SIZE-3, y+3), (x+3, y+CELL_SIZE-3), 3)


def is_valid_start_position(grid, row, col, ship_size, orientation):
    if orientation == 0: # horizontal
        for i in range(row-1, row+2):
            if i < 0 or i > 9:
                continue
            for j in range(col-1, col+ship_size+1):
                if j >= 0 and j <= 9:
                    if grid[i][j] == 2:
                        return False
    else:
        for i in range(row-1, row+ship_size+1):
            if i < 0 or i > 9:
                continue
            for j in range(col-1, col+2):
                if j >= 0 and j <= 9:
                    if grid[i][j] == 2:
                        return False
    return True
def place_ship(grid, ship_size):
    ship_orientation = random.randint(0, 1)
    new_grid = copy.deepcopy(grid)

    if ship_orientation == 0:  # horizontal
        ship_col = random.randint(0, 10 - ship_size)
        ship_row = random.randint(0, 9)
        while not is_valid_start_position(new_grid, ship_row, ship_col, ship_size, ship_orientation):
            ship_col = random.randint(0, 10 - ship_size)
            ship_row = random.randint(0, 9)

        new_grid[ship_row][ship_col] = 2

        for j in range(ship_size - 1):
            new_grid[ship_row][ship_col + j + 1] = 2
    else:  # vertical
        ship_col = random.randint(0, 9)
        ship_row = random.randint(0, 10 - ship_size)
        while not is_valid_start_position(new_grid, ship_row, ship_col, ship_size, ship_orientation):
            ship_col = random.randint(0, 9)
            ship_row = random.randint(0, 10 - ship_size)

        new_grid[ship_row][ship_col] = 2

        for j in range(ship_size - 1):
            new_grid[ship_row + j + 1][ship_col] = 2

    # grid = copy.deepcopy(new_grid)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            grid[i][j] = new_grid[i][j]

    return True


def place_ships(grid, ship_sizes):
    for size in ship_sizes:
        while not place_ship(grid, size):
            pass


def generate_coords(grid):
    row = random.randint(0, 9)
    col = random.randint(0, 9)
    while grid[row][col] == 1 or grid[row][col] == 3:
        row = random.randint(0, 9)
        col = random.randint(0, 9)

    return row, col


def is_killed(grid, row, col):
    ship_cells = [(row, col)]

    temp_row = row - 1
    while temp_row >= 0 and grid[temp_row][col] != 0 and grid[temp_row][col] != 1:
        ship_cells.append((temp_row, col))
        temp_row -= 1

    temp_row = row + 1
    while temp_row <= 9 and grid[temp_row][col] != 0 and grid[temp_row][col] != 1:
        ship_cells.append((temp_row, col))
        temp_row += 1

    temp_col = col - 1
    while temp_col >= 0 and grid[row][temp_col] != 0 and grid[row][temp_col] != 1:
        ship_cells.append((row, temp_col))
        temp_col -= 1

    temp_col = col + 1
    while temp_col <= 9 and grid[row][temp_col] != 0 and grid[row][temp_col] != 1:
        ship_cells.append((row, temp_col))
        temp_col += 1

    for cell in ship_cells:
        if grid[cell[0]][cell[1]] == 2:
            return False

    if len(ship_cells) == 1 or ship_cells[0][0] == ship_cells[1][0]:  # horizontal
        ship_begin_col = 9
        for cell in ship_cells:
            if cell[1] < ship_begin_col:
                ship_begin_col = cell[1]

        for i in range(row-1, row+2):
            if i < 0 or i > 9:
                continue
            for j in range(ship_begin_col-1, ship_begin_col + len(ship_cells) + 1):
                if grid[i][j] == 0:
                    grid[i][j] = 1
    else:  # vertical
        ship_begin_row = 9
        for cell in ship_cells:
            if cell[0] < ship_begin_row:
                ship_begin_row = cell[0]

        for i in range(ship_begin_row - 1, ship_begin_row + len(ship_cells) + 1):
            if i < 0 or i > 9:
                continue
            for j in range(col - 1, col + 2):
                if grid[i][j] == 0:
                    grid[i][j] = 1
    return True


def shoot(grid, row, col):
    if grid[row][col] == 0:
        grid[row][col] = 1
        return 1  # miss
    elif grid[row][col] == 2:
        grid[row][col] = 3
        if row - 1 >= 0 and col - 1 >= 0:
            grid[row - 1][col - 1] = 1
        if row - 1 >= 0 and col + 1 <= 9:
            grid[row - 1][col + 1] = 1
        if row + 1 <= 9 and col + 1 <= 9:
            grid[row + 1][col + 1] = 1
        if row + 1 <= 9 and col - 1 >= 0:
            grid[row + 1][col - 1] = 1

        is_killed(grid, row, col)

    return 0  # hit


ICON = pygame.image.load("icon.png")
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Battleship")
pygame.display.set_icon(ICON)

run = True
turn = 0  # 0, 2, 4 - player;  1,3,5 - computer

place_ships(computer_grid, SHIP_SIZES)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if turn%2 == 0:
                if x > COMPUTER_GRID_RIGHT_MARGIN and x < COMPUTER_GRID_RIGHT_MARGIN+GRID_SIZE*(CELL_SIZE+MARGIN) and y > COMPUTER_GRID_TOP_MARGIN+CELL_SIZE and y < COMPUTER_GRID_TOP_MARGIN+(GRID_SIZE+1)*(CELL_SIZE+MARGIN):
                    row = (y-COMPUTER_GRID_TOP_MARGIN-CELL_SIZE-MARGIN) // (CELL_SIZE + MARGIN)
                    col = (x-COMPUTER_GRID_RIGHT_MARGIN-MARGIN) // (CELL_SIZE + MARGIN)

                    turn += shoot(computer_grid, row, col)
                    print(f"Player: {row}, {col}")
            # else:
            #     if x > PLAYER_GRID_RIGHT_MARGIN and x < PLAYER_GRID_RIGHT_MARGIN+GRID_SIZE*(CELL_SIZE+MARGIN) and y > PLAYER_GRID_TOP_MARGIN+CELL_SIZE and y < PLAYER_GRID_TOP_MARGIN+(GRID_SIZE+1)*(CELL_SIZE+MARGIN):
            #         row = (y - PLAYER_GRID_TOP_MARGIN-CELL_SIZE-MARGIN) // (CELL_SIZE + MARGIN)
            #         col = (x - PLAYER_GRID_RIGHT_MARGIN-MARGIN) // (CELL_SIZE + MARGIN)
            #
            #         if player_grid[row][col] == 0:
            #             player_grid[row][col] = 1
            #
            #             turn += 1
    if turn % 2 == 1:
        print("Here computer generate coords")
        row, col = generate_coords(player_grid)
        print(f"Computer: {row}, {col}")
        turn += shoot(player_grid, row, col)

    screen.fill(BACKGROUND_COLOR)
    display_grid(player_grid, PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN)
    display_grid(computer_grid, COMPUTER_GRID_RIGHT_MARGIN, COMPUTER_GRID_TOP_MARGIN)

    you = font.render("You", True, BLACK)
    computer = font.render("Computer", True, BLACK)
    you_rect = you.get_rect(); computer_rect = computer.get_rect()
    you_rect.center = ((PLAYER_GRID_RIGHT_MARGIN*2+GRID_WIDTH)//2, PLAYER_GRID_TOP_MARGIN//2)
    computer_rect.center = ((COMPUTER_GRID_RIGHT_MARGIN*2+GRID_WIDTH)//2, COMPUTER_GRID_TOP_MARGIN//2)
    screen.blit(you, you_rect)
    screen.blit(computer, computer_rect)


    pygame.display.update()
