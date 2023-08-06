from grid import *

SELECTED_COLOR = RED

CELL_SIZE = 30
MARGIN = 1


class Ship:
    def __init__(self, screen, left_margin, top_margin, size):
        self.__screen = screen
        self.__left_margin = left_margin
        self.__top_margin = top_margin
        self.__size = size
        self.__orientation = HORIZONTAL
        self.__color = BLUE
        self.__length = self.__size * CELL_SIZE + (self.__size - 1) * MARGIN
        self.__selected = False

        if self.__orientation == HORIZONTAL:
            self.__surf = pygame.Surface((self.__length, CELL_SIZE))
        else:
            self.__surf = pygame.Surface((CELL_SIZE, self.__length))

        self.__surf.fill(self.__color)
        self.__rect = self.__surf.get_rect()
        self.__rect.left = self.__left_margin
        self.__rect.top = self.__top_margin
        # if self.__orientation == HORIZONTAL:
        #     self.__rect = pygame.draw.rect(self.__screen, self.__color, (self.__left_margin, self.__top_margin, self.__length, CELL_SIZE))
        # else:
        #     self.__rect = pygame.draw.rect(self.__screen, self.__color, (self.__left_margin, self.__top_margin, CELL_SIZE, self.__length))
        pygame.display.update()

    def display(self):

        self.__screen.blit(self.__surf, [self.__left_margin, self.__top_margin])
        # if self.__orientation == HORIZONTAL:
        #     pygame.draw.rect(self.__screen, self.__color, (self.__left_margin, self.__top_margin, self.__length, CELL_SIZE))
        # else:
        #     pygame.draw.rect(self.__screen, self.__color, (self.__left_margin, self.__top_margin, CELL_SIZE, self.__length))

        # self.__rect.move(self.__left_margin, self.__top_margin)
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

    def select(self):
        self.__selected = True
        self.__color = SELECTED_COLOR
        self.__surf.fill(self.__color)
        self.display()

    def undo_selection(self):
        self.__selected = False
        self.__color = BLUE
        self.__surf.fill(self.__color)
        self.display()

    def belongs(self, x, y):
        if x >= self.left() and x <= self.right() and y >= self.top() and y <= self.bottom():
            return True
        return False

    def is_selected(self):
        return self.__selected

    def get_orientation(self):
        return self.__orientation

    def get_size(self):
        return self.__size

    def set_left(self, left_margin):
        self.__left_margin = left_margin

    def set_top(self, top_margin):
        self.__top_margin = top_margin

    def turn(self):
        if self.__orientation == HORIZONTAL:
            self.__orientation = VERTICAL
            self.__surf = pygame.transform.rotate(self.__surf, 90)
            # self.__rect = pygame.draw.rect(self.__screen, self.__color,
            #                                (self.__left_margin, self.__top_margin, CELL_SIZE, self.__length))

        else:
            self.__orientation = HORIZONTAL
            self.__surf = pygame.transform.rotate(self.__surf, -90)

            # self.__rect = pygame.draw.rect(self.__screen, self.__color, (self.__left_margin, self.__top_margin, self.__length, CELL_SIZE))

    def length(self):
        return self.__length
