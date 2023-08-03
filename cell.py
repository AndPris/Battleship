EMPTY_CELL = 0
MISS_CELL = 1
SHIP_CELL = 2
CRASHED_SHIP_CELL = 3


class Cell:
    def __init__(self, row, col):
        self.__state = EMPTY_CELL
        self.__row = row
        self.__col = col
        self.__ship = None

    def set_ship(self, ship):
        self.__ship = ship
        self.__state = SHIP_CELL

    def get_ship(self):
        return self.__ship

    def get_state(self):
        return self.__state

    def shoot(self):
        if self.__state == EMPTY_CELL:
            self.__state = MISS_CELL
        elif self.__state == SHIP_CELL:
            self.__state = CRASHED_SHIP_CELL
