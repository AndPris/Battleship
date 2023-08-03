import copy
import random

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
player_grid.randomly_place_ships(SHIP_SIZES)


def generate_coords():
    row = random.randint(0, GRID_SIZE-1)
    col = random.randint(0, GRID_SIZE-1)

    return row, col

def smart_generate_coords(grid, row, col):
    probable_ship_cells = []


    if (row - 1 >= 0 and grid.get_cell_value(row-1, col) == CRASHED_SHIP_CELL) or (row + 1 <= GRID_SIZE-1 and grid.get_cell_value(row+1, col) == CRASHED_SHIP_CELL):
        print("If")
        temp_row = row - 1
        while temp_row >= 0 and grid.get_cell_value(temp_row, col) == CRASHED_SHIP_CELL:
            temp_row -= 1

        if temp_row >= 0 and grid.get_cell_value(temp_row, col) != MISS_CELL:
            probable_ship_cells.append((temp_row, col))

        temp_row = row + 1
        while temp_row <= GRID_SIZE-1 and grid.get_cell_value(temp_row, col) == CRASHED_SHIP_CELL:
            temp_row += 1

        if temp_row <= GRID_SIZE-1 and grid.get_cell_value(temp_row, col) != MISS_CELL:
            probable_ship_cells.append((temp_row, col))

    elif (col - 1 >= 0 and grid.get_cell_value(row, col-1) == CRASHED_SHIP_CELL) or (col + 1 <= GRID_SIZE-1 and grid.get_cell_value(row, col+1) == CRASHED_SHIP_CELL):
        print("Elif")
        temp_col = col - 1
        while temp_col >= 0 and grid.get_cell_value(row, temp_col) == CRASHED_SHIP_CELL:
            temp_col -= 1

        if temp_col >= 0 and grid.get_cell_value(row, temp_col) != MISS_CELL:
            probable_ship_cells.append((row, temp_col))

        temp_col = col + 1
        while temp_col <= GRID_SIZE-1 and grid.get_cell_value(row, temp_col) == CRASHED_SHIP_CELL:
            temp_col += 1

        if temp_col <= GRID_SIZE-1 and grid.get_cell_value(row, temp_col) != MISS_CELL:
            probable_ship_cells.append((row, temp_col))
    else:
        print("Else")
        if col-1 >= 0 and grid.get_cell_value(row, col-1) != MISS_CELL:
            probable_ship_cells.append((row, col-1))
        if col+1 <= GRID_SIZE-1 and grid.get_cell_value(row, col+1) != MISS_CELL:
            probable_ship_cells.append((row, col+1))
        if row-1 >= 0 and grid.get_cell_value(row-1, col) != MISS_CELL:
            probable_ship_cells.append((row-1, col))
        if row+1 <= GRID_SIZE-1 and grid.get_cell_value(row+1, col) != MISS_CELL:
            probable_ship_cells.append((row+1, col))

    choice = probable_ship_cells[random.randint(0, len(probable_ship_cells)-1)]
    print(probable_ship_cells)
    print(choice)
    return choice

def display_screen():
    screen.fill(BACKGROUND_COLOR)
    computer_grid.display(screen, CELL_SIZE, MARGIN, COMPUTER_GRID_RIGHT_MARGIN, COMPUTER_GRID_TOP_MARGIN, MISS_RADIUS, CRASHED_SHIP_CELL)
    player_grid.display(screen, CELL_SIZE, MARGIN, PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN, MISS_RADIUS, CRASHED_SHIP_CELL)
    pygame.display.update()

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

is_killed = True
has_aim = False

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

                    result, not_used = computer_grid.shoot(row, col)
                    turn += result
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         place_ships(player_grid, SHIP_SIZES)
        #         display_screen()
        #         display_grid(player_grid, PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN, 2)
        #         pygame.display.update()
        #         pygame.time.wait(3000)
        #         place_ships(computer_grid, SHIP_SIZES)
        #         start = True

    # if start:
    #     # if check_win():
    #     #     pass
    #     # else:
    #     # display_screen()
    #
    #     pygame.display.update()

    if turn % 2 == 1:
        # pygame.time.wait(300)
        if not has_aim:
            row, col = generate_coords()
            result, is_killed = player_grid.shoot(row, col)
            if result == HIT_VALUE and not is_killed:
                anchor_row, anchor_col = row, col
                has_aim = True
        else:
            row, col = smart_generate_coords(player_grid, anchor_row, anchor_col)
            result, is_killed = player_grid.shoot(row, col)

            if is_killed:
                has_aim = False

        turn += result

    display_screen()
