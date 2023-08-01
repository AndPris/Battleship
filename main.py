import pygame
import random

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

PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN = (50, 50)
COMPUTER_GRID_RIGHT_MARGIN, COMPUTER_GRID_TOP_MARGIN = (50 + 11 * (CELL_SIZE + MARGIN) + 100, 50)

player_grid = [[0]*10 for i in range(10)]
computer_grid = [[0]*10 for i in range(10)]

font = pygame.font.SysFont("arial", CELL_SIZE + MARGIN)


def display_grid(grid, right_margin, top_margin):
    for row in range(GRID_SIZE):
        char = font.render(chr(row + 65), False, WHITE)
        num = font.render(str(row + 1), False, WHITE)

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

            if grid[row][col] == 1:
                pygame.draw.circle(screen, BLACK, [x + CELL_SIZE//2, y + CELL_SIZE//2], MISS_RADIUS, 0)
            elif grid[row][col] == 2:
                pygame.draw.line(screen, RED, (x+3, y+3), (x+CELL_SIZE-3, y+CELL_SIZE-3), 3)
                pygame.draw.line(screen, RED, (x+CELL_SIZE-3, y+3), (x+3, y+CELL_SIZE-3), 3)


ICON = pygame.image.load("icon.png")
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Battleship")
pygame.display.set_icon(ICON)

run = True
turn = 0  # 0, 2, 4 - player;  1,3,5 - computer
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if turn%2 == 0:
                if x > COMPUTER_GRID_RIGHT_MARGIN and x < COMPUTER_GRID_RIGHT_MARGIN+GRID_SIZE*(CELL_SIZE+MARGIN) and y > COMPUTER_GRID_TOP_MARGIN+CELL_SIZE and y < COMPUTER_GRID_TOP_MARGIN+(GRID_SIZE+1)*(CELL_SIZE+MARGIN):
                    row = (x-COMPUTER_GRID_RIGHT_MARGIN-MARGIN) // (CELL_SIZE + MARGIN)
                    col = (y-COMPUTER_GRID_TOP_MARGIN-CELL_SIZE-MARGIN) // (CELL_SIZE + MARGIN)

                    if computer_grid[row][col] == 0:
                        computer_grid[row][col] = 1
                        turn += 1
            else:
                if x > PLAYER_GRID_RIGHT_MARGIN and x < PLAYER_GRID_RIGHT_MARGIN+GRID_SIZE*(CELL_SIZE+MARGIN) and y > PLAYER_GRID_TOP_MARGIN+CELL_SIZE and y < PLAYER_GRID_TOP_MARGIN+(GRID_SIZE+1)*(CELL_SIZE+MARGIN):
                    row = (x - PLAYER_GRID_RIGHT_MARGIN-MARGIN) // (CELL_SIZE + MARGIN)
                    col = (y - PLAYER_GRID_TOP_MARGIN-CELL_SIZE-MARGIN) // (CELL_SIZE + MARGIN)

                    if player_grid[row][col] == 0:
                        player_grid[row][col] = 1
                        turn += 1

    screen.fill(BACKGROUND_COLOR)
    display_grid(player_grid, PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN)
    display_grid(computer_grid, COMPUTER_GRID_RIGHT_MARGIN, COMPUTER_GRID_TOP_MARGIN)

    pygame.display.update()
