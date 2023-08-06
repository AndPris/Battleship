from shoot_logic import *
from ship import *


pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
GRID_SIZE = 10
GRID_WIDTH = 11 * (CELL_SIZE + MARGIN)
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN = (50, 120)
COMPUTER_GRID_LEFT_MARGIN, COMPUTER_GRID_TOP_MARGIN = (PLAYER_GRID_LEFT_MARGIN + GRID_WIDTH + 100, PLAYER_GRID_TOP_MARGIN)

ICON = pygame.image.load("icon.png")
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Battleship")
pygame.display.set_icon(ICON)


player_grid = Grid(GRID_SIZE, "You")
computer_grid = Grid(GRID_SIZE, "Computer")
computer_grid.randomly_place_ships(SHIP_SIZES)


def draw_start_button(btn_top_margin, btn_left_margin, btn_width, btn_height):
    font = pygame.font.SysFont("arial", CELL_SIZE * 2)
    text = font.render("Start", True, BLUE)
    text_rect = text.get_rect()

    text_rect.top = btn_top_margin
    text_rect.left = btn_left_margin
    btn = pygame.draw.rect(screen, GREEN, (btn_left_margin, btn_top_margin, btn_width, btn_height))
    screen.blit(text, text_rect)
    pygame.display.update()
    return btn


def draw_random_place_ships_button():
    pass


def display_screen():
    win_text = None
    font = pygame.font.SysFont("arial", CELL_SIZE * 2)

    screen.fill(BACKGROUND_COLOR)
    computer_grid.display(screen, CELL_SIZE, MARGIN, COMPUTER_GRID_LEFT_MARGIN, COMPUTER_GRID_TOP_MARGIN, MISS_RADIUS)
    player_grid.display(screen, CELL_SIZE, MARGIN, PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN, MISS_RADIUS, True)

    if computer_grid.is_loose():
        win_text = font.render("You win!", True, GREEN)
    elif player_grid.is_loose():
        win_text = font.render("Computer wins :(", True, RED)

    if win_text is not None:
        # pygame.time.wait(1000)
        win_text_rect = win_text.get_rect()
        win_text_rect.center = ((COMPUTER_GRID_LEFT_MARGIN + GRID_WIDTH)//2, PLAYER_GRID_TOP_MARGIN // 2)
        screen.blit(win_text, win_text_rect)
    pygame.display.update()

    if win_text is None:
        return False
    return True


# def display_ships(ships):
#     for ship in ships:
#         ship.display()


SHIP_MARGIN = 5
display_screen()


def draw_ships(left_margin, top_margin):
    four_deck_ship1 = Ship(screen, left_margin, top_margin, 4)

    three_deck_ship1 = Ship(screen, four_deck_ship1.left(), four_deck_ship1.bottom()+SHIP_MARGIN, 3)
    three_deck_ship2 = Ship(screen, three_deck_ship1.right()+SHIP_MARGIN, three_deck_ship1.top(), 3)

    two_deck_ship1 = Ship(screen, four_deck_ship1.left(), three_deck_ship1.bottom()+SHIP_MARGIN, 2)
    two_deck_ship2 = Ship(screen, two_deck_ship1.right()+SHIP_MARGIN, two_deck_ship1.top(), 2)
    two_deck_ship3 = Ship(screen, two_deck_ship2.right()+SHIP_MARGIN, two_deck_ship1.top(), 2)

    one_deck_ship1 = Ship(screen, four_deck_ship1.left(), two_deck_ship1.bottom()+SHIP_MARGIN, 1)
    one_deck_ship2 = Ship(screen, one_deck_ship1.right()+SHIP_MARGIN, one_deck_ship1.top(), 1)
    one_deck_ship3 = Ship(screen, one_deck_ship2.right()+SHIP_MARGIN, one_deck_ship1.top(), 1)
    one_deck_ship4 = Ship(screen, one_deck_ship3.right()+SHIP_MARGIN, one_deck_ship1.top(), 1)

    ships = [four_deck_ship1, three_deck_ship1, three_deck_ship2, two_deck_ship1, two_deck_ship2, two_deck_ship3,
             one_deck_ship1, one_deck_ship2, one_deck_ship3, one_deck_ship4]

    return ships


pygame.display.update()
player_ships = draw_ships(PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN+GRID_WIDTH+CELL_SIZE)


run = True
start = False
turn = 0  # 0, 2, 4 - player;  1,3,5 - computer
game_over = False
is_killed = True
has_aim = False

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if not start and start_button.collidepoint(x, y) and player_grid.is_ships_placed():
                start = True

            if not game_over and start:
                if turn%2 == 0:
                    if computer_grid.belongs(x, y):
                        row, col = computer_grid.get_coords(x, y)

                        result, not_used = computer_grid.shoot(row, col)
                        turn += result
            elif not start:
                for ship in player_ships:
                    if ship.is_selected() and player_grid.belongs(x, y):
                        row, col = player_grid.get_coords(x, y)

                        if player_grid.is_valid_start_position(row, col, ship.get_size(), ship.get_orientation()):
                            player_grid.place_ship(row, col, ship.get_size(), ship.get_orientation())
                            precise_x, precise_y = player_grid.get_precise_coords(x, y)
                            ship.set_left(precise_x)
                            ship.set_top(precise_y)
                            display_screen()
                            for ship2 in player_ships:
                                ship2.undo_selection()
                    elif ship.belongs(x, y) and not player_grid.belongs(x, y):
                        ship.select()
                    else:
                        ship.undo_selection()
                    # if ship.is_selected() and player_grid.belongs(x, y):
                    #     for ship2 in player_ships:
                    #         if ship2.belongs(x, y):
                    #             ship2.select()
                    #             ship.undo_selection()
                    #
                    #     row, col = player_grid.get_coords(x, y)
                    #
                    #     if player_grid.is_valid_start_position(row, col, ship.get_size(), ship.get_orientation()):
                    #         player_grid.place_ship(row, col, ship.get_size(), ship.get_orientation())
                    #         precise_x, precise_y = player_grid.get_precise_coords(x, y)
                    #         ship.set_left(precise_x)
                    #         ship.set_top(precise_y)
                    #         display_screen()
                    #         for ship2 in player_ships:
                    #             ship2.undo_selection()
                    #     else:
                    #         ship.undo_selection()
                    # else:
                    #     if ship.belongs(x, y):
                    #         if player_grid.belongs(x, y):
                    #             for i in range(ship.get_size()):
                    #                 if ship.get_orientation() == HORIZONTAL:
                    #                     player_grid.set_cell_value(row, col + i, EMPTY_CELL)
                    #                 else:
                    #                     player_grid.set_cell_value(row + i, col, EMPTY_CELL)
                    #         ship.select()
                    #     else:
                    #         ship.undo_selection()

    if not start:
        start_button = draw_start_button(PLAYER_GRID_TOP_MARGIN, COMPUTER_GRID_LEFT_MARGIN + GRID_WIDTH, CELL_SIZE*4, CELL_SIZE*2)
        continue

    if not game_over and turn % 2 == 1:
        # pygame.time.wait(300)
        if not has_aim:
            row, col = generate_coords(GRID_SIZE)
            result, is_killed = player_grid.shoot(row, col)
            if result == HIT_VALUE and not is_killed:
                anchor_row, anchor_col = row, col
                has_aim = True
        else:
            row, col = smart_generate_coords(player_grid, anchor_row, anchor_col, GRID_SIZE)
            result, is_killed = player_grid.shoot(row, col)

            if is_killed:
                has_aim = False

        turn += result

    game_over = display_screen()
