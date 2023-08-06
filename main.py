from shoot_logic import *
from ship import *
from button import *

pygame.init()

GAME_WITH_COMPUTER = "single"
GAME_WITH_FRIEND = "multiplayer"

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
GRID_SIZE = 10
GRID_WIDTH = 11 * (CELL_SIZE + MARGIN)
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
SHIP_MARGIN = 5

PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN = (50, 120)
COMPUTER_GRID_LEFT_MARGIN, COMPUTER_GRID_TOP_MARGIN = (
    PLAYER_GRID_LEFT_MARGIN + GRID_WIDTH + 100, PLAYER_GRID_TOP_MARGIN)

ICON = pygame.image.load("icon.png")
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Battleship")
pygame.display.set_icon(ICON)
screen.fill(BACKGROUND_COLOR)

player_grid = Grid(GRID_SIZE, "You")
computer_grid = Grid(GRID_SIZE, "Computer")
computer_grid.randomly_place_ships(SHIP_SIZES)


def draw_ships(left_margin, top_margin):
    four_deck_ship1 = Ship(screen, left_margin, top_margin, 4)

    three_deck_ship1 = Ship(screen, four_deck_ship1.right() + SHIP_MARGIN, four_deck_ship1.top(), 3)
    three_deck_ship2 = Ship(screen, three_deck_ship1.right() + SHIP_MARGIN, three_deck_ship1.top(), 3)

    two_deck_ship1 = Ship(screen, three_deck_ship2.right() + SHIP_MARGIN, three_deck_ship2.top(), 2)
    two_deck_ship2 = Ship(screen, two_deck_ship1.right() + SHIP_MARGIN, two_deck_ship1.top(), 2)
    two_deck_ship3 = Ship(screen, two_deck_ship2.right() + SHIP_MARGIN, two_deck_ship1.top(), 2)

    one_deck_ship1 = Ship(screen, two_deck_ship3.right() + SHIP_MARGIN, two_deck_ship1.top(), 1)
    one_deck_ship2 = Ship(screen, one_deck_ship1.right() + SHIP_MARGIN, one_deck_ship1.top(), 1)
    one_deck_ship3 = Ship(screen, one_deck_ship2.right() + SHIP_MARGIN, one_deck_ship1.top(), 1)
    one_deck_ship4 = Ship(screen, one_deck_ship3.right() + SHIP_MARGIN, one_deck_ship1.top(), 1)

    ships = [four_deck_ship1, three_deck_ship1, three_deck_ship2, two_deck_ship1, two_deck_ship2, two_deck_ship3,
             one_deck_ship1, one_deck_ship2, one_deck_ship3, one_deck_ship4]

    return ships


player_ships = draw_ships(PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN + GRID_WIDTH + CELL_SIZE)


def display_ships(ships):
    for ship in ships:
        ship.display()


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
        win_text_rect = win_text.get_rect()
        win_text_rect.center = ((COMPUTER_GRID_LEFT_MARGIN + GRID_WIDTH) // 2, PLAYER_GRID_TOP_MARGIN // 2)
        screen.blit(win_text, win_text_rect)

    pygame.display.update()

    if win_text is None:
        return False
    return True


game_mode = None

welcome_buttons = []


def set_single_mode():
    global game_mode
    game_mode = GAME_WITH_COMPUTER
    welcome_buttons.clear()
    display_screen()
    pygame.display.update()



def set_multiplayer_mode():
    pass
    # global game_mode
    # game_mode = GAME_WITH_FRIEND


WELCOME_BUTTON_WIDTH = CELL_SIZE * 8
WELCOME_BUTTON_HEIGHT = CELL_SIZE * 4

single_mode_button = Button(screen, (SCREEN_WIDTH - WELCOME_BUTTON_WIDTH) // 2,
                            SCREEN_HEIGHT // 2 - WELCOME_BUTTON_HEIGHT,
                            WELCOME_BUTTON_WIDTH, WELCOME_BUTTON_HEIGHT, 35,
                            "Play with computer", set_single_mode)
multiplayer_mode_buttons = Button(screen, single_mode_button.x,
                                  single_mode_button.y + single_mode_button.height + CELL_SIZE,
                                  WELCOME_BUTTON_WIDTH, WELCOME_BUTTON_HEIGHT, 18,
                                  "Play with friend (not implemented)", set_multiplayer_mode)
welcome_buttons.append(single_mode_button)
welcome_buttons.append(multiplayer_mode_buttons)

run = True
start = False
turn = 0  # 0, 2, 4 - player;  1,3,5 - computer
game_over = False
is_killed = True
has_aim = False


def start_game():
    global start
    if player_grid.is_ships_placed():
        start = True


def randomly_place_players_ships():
    player_grid.clear()
    player_grid.randomly_place_ships(SHIP_SIZES)
    display_screen()
    player_ships.clear()


def clear():
    global player_ships
    player_grid.clear()
    display_screen()
    player_ships = draw_ships(PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN + GRID_WIDTH + CELL_SIZE)


font_size = 25
start_buttons = []
start_button = Button(screen, COMPUTER_GRID_LEFT_MARGIN + GRID_WIDTH, PLAYER_GRID_TOP_MARGIN, CELL_SIZE * 4,
                      CELL_SIZE * 2, font_size, "Start", start_game)
random_place_ships_button = Button(screen, start_button.x, start_button.y + start_button.height + SHIP_MARGIN,
                                   start_button.width, start_button.height, font_size, "Random",
                                   randomly_place_players_ships)
clear_button = Button(screen, random_place_ships_button.x,
                      random_place_ships_button.y + random_place_ships_button.height + SHIP_MARGIN,
                      random_place_ships_button.width, random_place_ships_button.height, font_size, "Clear", clear)

start_buttons.append(start_button)
start_buttons.append(random_place_ships_button)
start_buttons.append(clear_button)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if game_mode is None:
            for button in welcome_buttons:
                button.process()
                pygame.display.update()

            if game_mode is not None:
                display_screen()
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if not game_over and start:
                if turn % 2 == 0:
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
                            player_ships.remove(ship)
                    elif ship.belongs(x, y) and not player_grid.belongs(x, y):
                        for ship2 in player_ships:
                            ship2.undo_selection()
                        ship.select()
                    else:
                        ship.undo_selection()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            for ship in player_ships:
                if ship.is_selected():
                    ship.turn()
                display_screen()

    if game_mode is None:
        continue

    if not start:
        is_selected_available = False
        for ship in player_ships:
            if ship.is_selected():
                is_selected_available = True
                break
        if not is_selected_available and len(player_ships) != 0:
            player_ships[0].select()

        display_ships(player_ships)
        for btn in start_buttons:
            btn.process()
        pygame.display.update()
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
