import copy
from grid import *

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
GRID_SIZE = 10
CELL_SIZE = 30
MARGIN = 1
MISS_RADIUS = 5
GRID_WIDTH = 11 * (CELL_SIZE + MARGIN)
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN = (50, 100)
COMPUTER_GRID_RIGHT_MARGIN, COMPUTER_GRID_TOP_MARGIN = (PLAYER_GRID_RIGHT_MARGIN + GRID_WIDTH + 100, PLAYER_GRID_TOP_MARGIN)

ICON = pygame.image.load("icon.png")
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Battleship")
pygame.display.set_icon(ICON)


player_grid = Grid(GRID_SIZE, "You")
computer_grid = Grid(GRID_SIZE, "Computer")
computer_grid.randomly_place_ships(SHIP_SIZES)

screen.fill(BACKGROUND_COLOR)
computer_grid.display(screen, CELL_SIZE, MARGIN, COMPUTER_GRID_RIGHT_MARGIN, COMPUTER_GRID_TOP_MARGIN, MISS_RADIUS, 2)
player_grid.display(screen, CELL_SIZE, MARGIN, PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN, MISS_RADIUS, 2)

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
                if j < 0 or j > 9:
                    continue

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
                if j < 0 or j > 9:
                    continue

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


# def display_screen():
#     screen.fill(BACKGROUND_COLOR)
#     display_grid(player_grid, PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN, 3)
#     display_grid(computer_grid, COMPUTER_GRID_RIGHT_MARGIN, COMPUTER_GRID_TOP_MARGIN, 3)
#
#     you = font.render("You", True, BLACK)
#     computer = font.render("Computer", True, BLACK)
#     you_rect = you.get_rect();
#     computer_rect = computer.get_rect()
#     you_rect.center = ((PLAYER_GRID_RIGHT_MARGIN * 2 + GRID_WIDTH) // 2, PLAYER_GRID_TOP_MARGIN // 2)
#     computer_rect.center = ((COMPUTER_GRID_RIGHT_MARGIN * 2 + GRID_WIDTH) // 2, COMPUTER_GRID_TOP_MARGIN // 2)
#     screen.blit(you, you_rect)
#     screen.blit(computer, computer_rect)

# def check_win():
#     player_win = True
#     computer_win = False
#
#     for i in range(GRID_SIZE):
#         for j in range(GRID_SIZE):
#             if computer_grid[i][j] == 2:
#                 player_win = False
#             if player_grid[i][j] == 2:
#                 computer_win = False
#
#     win_text = None
#     if player_win:
#         win_text = font.render("You win!", True, YELLOW)
#     elif computer_win:
#         win_text = font.render("Computer wins :(", True, RED)
#
#     if win_text is None:
#         return False
#
#     pygame.time.wait(1000)
#     screen.fill(BLACK)
#     win_text_rect = win_text.get_rect()
#     win_text_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
#     screen.blit(win_text, win_text_rect)
#
#     return True




run = True
start = True
turn = 0  # 0, 2, 4 - player;  1,3,5 - computer

# welcome_text = font.render("Press space to start game", True, BLACK)
# screen.fill(WHITE)
# welcome_text_rect = welcome_text.get_rect()
# welcome_text_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
# screen.blit(welcome_text, welcome_text_rect)
# pygame.display.update()


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and start:
            if turn%2 == 0:
                x, y = pygame.mouse.get_pos()

                if x > COMPUTER_GRID_RIGHT_MARGIN and x < COMPUTER_GRID_RIGHT_MARGIN+GRID_SIZE*(CELL_SIZE+MARGIN) and y > COMPUTER_GRID_TOP_MARGIN+CELL_SIZE and y < COMPUTER_GRID_TOP_MARGIN+(GRID_SIZE+1)*(CELL_SIZE+MARGIN):
                    row = (y-COMPUTER_GRID_TOP_MARGIN-CELL_SIZE-MARGIN) // (CELL_SIZE + MARGIN)
                    col = (x-COMPUTER_GRID_RIGHT_MARGIN-MARGIN) // (CELL_SIZE + MARGIN)

                    turn += shoot(computer_grid, row, col)
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         place_ships(player_grid, SHIP_SIZES)
        #         display_screen()
        #         display_grid(player_grid, PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN, 2)
        #         pygame.display.update()
        #         pygame.time.wait(3000)
        #         place_ships(computer_grid, SHIP_SIZES)
        #         start = True

    if start:
        # if check_win():
        #     pass
        # else:
        # display_screen()

        pygame.display.update()

        if turn % 2 == 1:
            pygame.time.wait(300)
            row, col = generate_coords(player_grid)
            turn += shoot(player_grid, row, col)
