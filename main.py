import pygame
import random

pygame.init()

WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


SCREEN_SIZE = (1000, 500)
GRID_SIZE = 10
CELL_SIZE = 30
MARGIN = 1

font = pygame.font.SysFont("arial", CELL_SIZE + MARGIN)


def display_grid(right_margin, top_margin):
    for row in range(GRID_SIZE):
        char = font.render(chr(row + 65), False, WHITE)
        num = font.render(str(row+1), False, WHITE)

        char_rect = char.get_rect()
        num_rect = num.get_rect()
        # char_rect.center = (right_margin + (row + 1) * (MARGIN + CELL_SIZE) // 2, top_margin + CELL_SIZE//2)
        char_rect.top = top_margin
        char_rect.right = right_margin + (row + 1) * (MARGIN + CELL_SIZE) - 7
        num_rect.top = top_margin + (row + 1) * (MARGIN + CELL_SIZE)
        num_rect.right = right_margin

        screen.blit(char, char_rect)
        screen.blit(num, num_rect)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = right_margin + (row + 1) * MARGIN + row * CELL_SIZE
            y = top_margin + (col + 1) * (MARGIN + CELL_SIZE)
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))


ICON = pygame.image.load("icon.png")
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Battleship")
pygame.display.set_icon(ICON)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    display_grid(50, 50)
    display_grid(50 + 11 * (CELL_SIZE + MARGIN) + 100, 50)

    pygame.display.update()
