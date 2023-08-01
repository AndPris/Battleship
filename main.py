import pygame
import random

pygame.init()


ICON = pygame.image.load("icon.png")
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Battleship")
pygame.display.set_icon(ICON)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
