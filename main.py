import pygame

from shoot_logic import *
from ship import *
from button import *

pygame.init()

GAME_WITH_COMPUTER = "single"
GAME_WITH_FRIEND = "multiplayer"

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
GRID_SIZE = 10
GRID_WIDTH = 11 * (CELL_SIZE + MARGIN)
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
SHIP_MARGIN = 5

PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN = (50, 120)
COMPUTER_GRID_LEFT_MARGIN, COMPUTER_GRID_TOP_MARGIN = (
    PLAYER_GRID_LEFT_MARGIN + GRID_WIDTH + 150, PLAYER_GRID_TOP_MARGIN)

ICON = pygame.image.load("icon.png")
ROSE_ICON = pygame.image.load("rose.jpg")
ROSE_HEIGHT = ROSE_WIDTH = 200
ROSE_ICON = pygame.transform.scale(ROSE_ICON, (ROSE_WIDTH, ROSE_HEIGHT))
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Battleship")
pygame.display.set_icon(ICON)
screen.fill(BACKGROUND_COLOR)

player_grid = Grid(GRID_SIZE, "You")
computer_grid = Grid(GRID_SIZE, "Computer")

game_mode = None
FIRST_PLAYER = 0; SECOND_PLAYER = 1
ships_placement_queue = FIRST_PLAYER  # 0 - first player, 1 - second


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


def display_screen(show_player_ships=False, show_computer_ships=False):
    if not game_over:
        win_text = None
    font = pygame.font.SysFont("arial", CELL_SIZE * 2)

    screen.fill(BACKGROUND_COLOR)
    computer_grid.display(screen, CELL_SIZE, MARGIN, COMPUTER_GRID_LEFT_MARGIN, COMPUTER_GRID_TOP_MARGIN, MISS_RADIUS, show_computer_ships)
    screen.blit(ROSE_ICON, (SCREEN_WIDTH-ROSE_WIDTH-20, SCREEN_HEIGHT-ROSE_HEIGHT-20))
    
    if game_mode == GAME_WITH_COMPUTER:
        player_grid.display(screen, CELL_SIZE, MARGIN, PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN, MISS_RADIUS,
                            True)
        if computer_grid.is_loose():
            win_text = font.render("You win!", True, (15, 101, 20))
        elif player_grid.is_loose():
            win_text = font.render("Computer wins :(", True, RED)
    elif game_mode == GAME_WITH_FRIEND:
        player_grid.display(screen, CELL_SIZE, MARGIN, PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN, MISS_RADIUS, show_player_ships)
        if computer_grid.is_loose():
            win_text = font.render("Player 1 wins!", True, (15, 101, 20))
        elif player_grid.is_loose():
            win_text = font.render("Player 2 wins!", True, RED)

    if win_text is not None:
        restart_text = font.render("Press space to restart game", True, BLUE)
        restart_text_rect = restart_text.get_rect()

        win_text_rect = win_text.get_rect()
        win_text_rect.center = ((COMPUTER_GRID_LEFT_MARGIN + GRID_WIDTH) // 2, PLAYER_GRID_TOP_MARGIN // 2)
        restart_text_rect.center = (win_text_rect.centerx, PLAYER_GRID_TOP_MARGIN+GRID_WIDTH+50)
        screen.blit(restart_text, restart_text_rect)
        screen.blit(win_text, win_text_rect)
        computer_grid.display(screen, CELL_SIZE, MARGIN, COMPUTER_GRID_LEFT_MARGIN, COMPUTER_GRID_TOP_MARGIN,
                              MISS_RADIUS, True)
        player_grid.display(screen, CELL_SIZE, MARGIN, PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN, MISS_RADIUS, True)


    pygame.display.update()

    if win_text is None:
        return False
    return True


run = True
start = False
turn = 0  # 0, 2, 4 - player;  1,3,5 - computer
game_over = False
is_killed = True
has_aim = False


def start_game():
    global start
    if player_grid.is_ships_placed() and computer_grid.is_ships_placed():
        start = True


def randomly_place_players_ships():
    if ships_placement_queue == FIRST_PLAYER:
        player_grid.clear()
        player_grid.randomly_place_ships(SHIP_SIZES)
        display_screen(True)
    else:
        computer_grid.clear()
        computer_grid.randomly_place_ships(SHIP_SIZES)
        display_screen(False, True)

    player_ships.clear()


def clear():
    global player_ships
    if ships_placement_queue == FIRST_PLAYER:
        player_grid.clear()
    else:
        computer_grid.clear()
    display_screen()
    player_ships = draw_ships(PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN + GRID_WIDTH + CELL_SIZE)


def place_ships(ships, grid, x, y, show_player=False, show_computer=False):
    for ship in ships:
        if ship.is_selected() and grid.belongs(x, y):
            row, col = grid.get_coords(x, y)

            if grid.is_valid_start_position(row, col, ship.get_size(), ship.get_orientation()):
                grid.place_ship(row, col, ship.get_size(), ship.get_orientation())
                precise_x, precise_y = grid.get_precise_coords(x, y)
                ship.set_left(precise_x)
                ship.set_top(precise_y)
                display_screen(show_player, show_computer)
                for ship2 in ships:
                    ship2.undo_selection()
                ships.remove(ship)
        elif ship.belongs(x, y) and not grid.belongs(x, y):
            for ship2 in ships:
                ship2.undo_selection()
            ship.select()
        else:
            ship.undo_selection()


def turn_ship(ships):
    for ship in ships:
        if ship.is_selected():
            ship.turn()

        if ships_placement_queue == FIRST_PLAYER:
            display_screen(True)
        else:
            display_screen(False, True)


def auto_select_ship(ships):
    is_selected_available = False
    for ship in ships:
        if ship.is_selected():
            is_selected_available = True
            break
    if not is_selected_available and len(ships) != 0:
        ships[0].select()

    display_ships(ships)


def process_buttons(buttons):
    for btn in buttons:
        btn.process()
    pygame.display.update()


def human_shoot(grid):
    global turn
    row, col = grid.get_coords(x, y)

    result, not_used = grid.shoot(row, col)
    turn += result


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


welcome_buttons = []


def set_single_mode():
    global game_mode
    game_mode = GAME_WITH_COMPUTER
    computer_grid.randomly_place_ships(SHIP_SIZES)
    welcome_buttons.clear()


def next_player():
    global ships_placement_queue, player_ships, player_grid
    if ships_placement_queue == SECOND_PLAYER or not player_grid.is_ships_placed():
        return

    ships_placement_queue = SECOND_PLAYER
    player_ships = draw_ships(PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN + GRID_WIDTH + CELL_SIZE)
    display_screen()


def set_multiplayer_mode():
    global game_mode, start_buttons
    player_grid.set_title("Player 1")
    computer_grid.set_title("Player 2")
    game_mode = GAME_WITH_FRIEND
    next_button = Button(screen, clear_button.x,
                      clear_button.y + clear_button.height + SHIP_MARGIN,
                      clear_button.width, clear_button.height, font_size, "Next", next_player)
    start_buttons.append(next_button)
    welcome_buttons.clear()


WELCOME_BUTTON_WIDTH = CELL_SIZE * 8
WELCOME_BUTTON_HEIGHT = CELL_SIZE * 4

single_mode_button = Button(screen, (SCREEN_WIDTH - WELCOME_BUTTON_WIDTH) // 2,
                            SCREEN_HEIGHT // 2 - WELCOME_BUTTON_HEIGHT,
                            WELCOME_BUTTON_WIDTH, WELCOME_BUTTON_HEIGHT, 35,
                            "Play with computer", set_single_mode)
multiplayer_mode_buttons = Button(screen, single_mode_button.x,
                                  single_mode_button.y + single_mode_button.height + CELL_SIZE,
                                  WELCOME_BUTTON_WIDTH, WELCOME_BUTTON_HEIGHT, 35,
                                  "Play with friend", set_multiplayer_mode)
welcome_buttons.append(single_mode_button)
welcome_buttons.append(multiplayer_mode_buttons)

screen.blit(ROSE_ICON, (single_mode_button.x + 20, single_mode_button.y - 10 - ROSE_HEIGHT))

while run:
    if game_mode is None:
        process_buttons(welcome_buttons)

        if game_mode is not None:
            display_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if game_mode == GAME_WITH_COMPUTER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if not game_over and start:
                    if turn % 2 == 0 and computer_grid.belongs(x, y):
                        human_shoot(computer_grid)
                elif not start:
                    place_ships(player_ships, player_grid, x, y)
            elif event.type == pygame.KEYDOWN:
                if not start and event.key == pygame.K_RIGHT:
                    turn_ship(player_ships)
                elif event.key == pygame.K_SPACE and game_over:
                    player_grid.clear()
                    computer_grid.clear()
                    computer_grid.randomly_place_ships(SHIP_SIZES)

                    start = False
                    game_over = False
                    turn = 0
                    player_ships = draw_ships(PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN + GRID_WIDTH + CELL_SIZE)
                    display_screen()
        elif game_mode == GAME_WITH_FRIEND:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if not game_over and start:
                    if turn % 2 == 0 and computer_grid.belongs(x, y):
                        human_shoot(computer_grid)
                    elif turn % 2 == 1 and player_grid.belongs(x, y):
                        human_shoot(player_grid)
                elif not start:
                    if ships_placement_queue == FIRST_PLAYER:
                        place_ships(player_ships, player_grid, x, y, True)
                    else:
                        place_ships(player_ships, computer_grid, x, y, False, True)
            elif event.type == pygame.KEYDOWN:
                if not start and event.key == pygame.K_RIGHT:
                    turn_ship(player_ships)
                elif event.key == pygame.K_SPACE and game_over:
                    player_grid.clear()
                    computer_grid.clear()

                    ships_placement_queue = FIRST_PLAYER
                    start = False
                    game_over = False
                    turn = 0
                    player_ships = draw_ships(PLAYER_GRID_LEFT_MARGIN, PLAYER_GRID_TOP_MARGIN + GRID_WIDTH + CELL_SIZE)
                    display_screen()

    if game_mode is None:
        continue

    if not start:
        auto_select_ship(player_ships)
        process_buttons(start_buttons)
        continue

    if game_mode == GAME_WITH_COMPUTER:
        if not game_over and turn % 2 == 1:
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
