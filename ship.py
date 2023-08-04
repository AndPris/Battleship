import pygame.display

from grid import *

BLUE = (0, 0, 255)
SELECTED_BLUE = (0, 0, 100)

CELL_SIZE = 30
MARGIN = 1


class Ship:
    def __init__(self, left_margin, top_margin, size):
        self.__left_margin = left_margin
        self.__top_margin = top_margin
        self.__size = size
        self.__orientation = HORIZONTAL
        self.__color = BLUE
        self.__length = self.__size * CELL_SIZE + (self.__size - 1) * MARGIN

    def display(self, screen):
        if self.__orientation == HORIZONTAL:
            pygame.draw.rect(screen, self.__color, (self.__left_margin, self.__top_margin, self.__length, CELL_SIZE))
        else:
            pygame.draw.rect(screen, self.__color, (self.__left_margin, self.__top_margin, CELL_SIZE, self.__length))

        pygame.display.update()

    def left(self):
        return self.__left_margin

    def right(self):
        if self.__orientation == HORIZONTAL:
            return self.__left_margin + self.__length
        return self.__left_margin + CELL_SIZE

    def top(self):
        return self.__top_margin

    def bottom(self):
        if self.__orientation == HORIZONTAL:
            return self.__top_margin+CELL_SIZE
        return self.__top_margin + self.__length
