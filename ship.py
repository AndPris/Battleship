from cell import *

HORIZONTAL = 0
VERTICAL = 1


class Ship:
    def __init__(self, anchor, size, orientation):
        self.__anchor = anchor
        self.__size = size
        self.__orientation = orientation

        self.__crashed_cells = []
        self.__occupied_cells = []
        for i in range(size):
            if self.__orientation == HORIZONTAL:
                self.__occupied_cells.append((anchor[0], anchor[1]+i))
            else:
                self.__occupied_cells.append((anchor[0]+i, anchor[1]))
