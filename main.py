from shoot_logic import *
from ship import *


pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
GRID_SIZE = 10
GRID_WIDTH = 11 * (CELL_SIZE + MARGIN)
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN = (50, 120)
COMPUTER_GRID_RIGHT_MARGIN, COMPUTER_GRID_TOP_MARGIN = (PLAYER_GRID_RIGHT_MARGIN + GRID_WIDTH + 100, PLAYER_GRID_TOP_MARGIN)

ICON = pygame.image.load("icon.png")
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Battleship")
pygame.display.set_icon(ICON)


player_grid = Grid(GRID_SIZE, "You")
computer_grid = Grid(GRID_SIZE, "Computer")
computer_grid.randomly_place_ships(SHIP_SIZES)
player_grid.randomly_place_ships(SHIP_SIZES)


def display_screen():
    win_text = None
    font = pygame.font.SysFont("arial", CELL_SIZE * 2)

    screen.fill(BACKGROUND_COLOR)
    computer_grid.display(screen, CELL_SIZE, MARGIN, COMPUTER_GRID_RIGHT_MARGIN, COMPUTER_GRID_TOP_MARGIN, MISS_RADIUS, CRASHED_SHIP_CELL)
    player_grid.display(screen, CELL_SIZE, MARGIN, PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN, MISS_RADIUS, CRASHED_SHIP_CELL)

    if computer_grid.is_loose():
        win_text = font.render("You win!", True, GREEN)
    elif player_grid.is_loose():
        win_text = font.render("Computer wins :(", True, RED)

    if win_text is not None:
        pygame.time.wait(1000)
        win_text_rect = win_text.get_rect()
        win_text_rect.center = (PLAYER_GRID_RIGHT_MARGIN + GRID_WIDTH, PLAYER_GRID_TOP_MARGIN // 2)
        screen.blit(win_text, win_text_rect)

    pygame.display.update()

    if win_text is None:
        return False
    return True


SHIP_MARGIN = 5
display_screen()


def draw_ships(left_margin, top_margin):
    four_deck_ship1 = Ship(left_margin, top_margin, 4) #pygame.draw.rect(screen, BLUE, (left_margin, top_margin, 4*(CELL_SIZE+MARGIN), CELL_SIZE))

    three_deck_ship1 = Ship(four_deck_ship1.left(), four_deck_ship1.bottom()+SHIP_MARGIN, 3) # pygame.draw.rect(screen, BLUE, (four_deck_ship1.left, four_deck_ship1.bottom+SHIP_MARGIN, 3*(CELL_SIZE+MARGIN), CELL_SIZE))
    three_deck_ship2 = Ship(three_deck_ship1.right()+SHIP_MARGIN, three_deck_ship1.top(), 3)  # pygame.draw.rect(screen, BLUE, (three_deck_ship1.right+SHIP_MARGIN, three_deck_ship1.top, 3*(CELL_SIZE+MARGIN), CELL_SIZE))

    two_deck_ship1 = Ship(four_deck_ship1.left(), three_deck_ship1.bottom()+SHIP_MARGIN, 2)  # pygame.draw.rect(screen, BLUE, (four_deck_ship1.left, three_deck_ship1.bottom+SHIP_MARGIN, 2*(CELL_SIZE+MARGIN), CELL_SIZE))
    two_deck_ship2 = Ship(two_deck_ship1.right()+SHIP_MARGIN, two_deck_ship1.top(), 2)#pygame.draw.rect(screen, BLUE, (two_deck_ship1.right+SHIP_MARGIN, two_deck_ship1.top, 2*(CELL_SIZE+MARGIN), CELL_SIZE))
    two_deck_ship3 = Ship(two_deck_ship2.right()+SHIP_MARGIN, two_deck_ship1.top(), 2)#pygame.draw.rect(screen, BLUE, (two_deck_ship2.right+SHIP_MARGIN, two_deck_ship1.top, 2*(CELL_SIZE+MARGIN), CELL_SIZE))

    one_deck_ship1 = Ship(four_deck_ship1.left(), two_deck_ship1.bottom()+SHIP_MARGIN, 1)#pygame.draw.rect(screen, BLUE, (four_deck_ship1.left, two_deck_ship1.bottom+SHIP_MARGIN, (CELL_SIZE+MARGIN), CELL_SIZE))
    one_deck_ship2 = Ship(one_deck_ship1.right()+SHIP_MARGIN, one_deck_ship1.top(), 1) #pygame.draw.rect(screen, BLUE, (one_deck_ship1.right+SHIP_MARGIN, one_deck_ship1.top, (CELL_SIZE+MARGIN), CELL_SIZE))
    one_deck_ship3 = Ship(one_deck_ship2.right()+SHIP_MARGIN, one_deck_ship1.top(), 1)#pygame.draw.rect(screen, BLUE, (one_deck_ship2.right+SHIP_MARGIN, one_deck_ship1.top, (CELL_SIZE+MARGIN), CELL_SIZE))
    one_deck_ship4 = Ship(one_deck_ship3.right()+SHIP_MARGIN, one_deck_ship1.top(), 1)  #pygame.draw.rect(screen, BLUE, (one_deck_ship3.right+SHIP_MARGIN, one_deck_ship1.top, (CELL_SIZE+MARGIN), CELL_SIZE))


    ships = [four_deck_ship1, three_deck_ship1, three_deck_ship2, two_deck_ship1, two_deck_ship2, two_deck_ship3,
             one_deck_ship1, one_deck_ship2, one_deck_ship3, one_deck_ship4]

    for ship in ships:
        ship.display(screen)

    return ships


pygame.display.update()
player_ships = draw_ships(PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN+GRID_WIDTH+CELL_SIZE)


run = True
start = False
turn = 0  # 0, 2, 4 - player;  1,3,5 - computer
game_over = False

# welcome_text = font.render("Press space to start game", True, BLACK)
# screen.fill(WHITE)
# welcome_text_rect = welcome_text.get_rect()
# welcome_text_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
# screen.blit(welcome_text, welcome_text_rect)
# pygame.display.update()

is_killed = True
has_aim = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and start:
            if turn%2 == 0:
                x, y = pygame.mouse.get_pos()

                if x > COMPUTER_GRID_RIGHT_MARGIN and x < COMPUTER_GRID_RIGHT_MARGIN+GRID_SIZE*(CELL_SIZE+MARGIN) and y > COMPUTER_GRID_TOP_MARGIN+CELL_SIZE and y < COMPUTER_GRID_TOP_MARGIN+(GRID_SIZE+1)*(CELL_SIZE+MARGIN):
                    row = (y-COMPUTER_GRID_TOP_MARGIN-CELL_SIZE-MARGIN) // (CELL_SIZE + MARGIN)
                    col = (x-COMPUTER_GRID_RIGHT_MARGIN-MARGIN) // (CELL_SIZE + MARGIN)

                    result, not_used = computer_grid.shoot(row, col)
                    turn += result
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         place_ships(player_grid, SHIP_SIZES)
        #         display_screen()
        #         display_grid(player_grid, PLAYER_GRID_RIGHT_MARGIN, PLAYER_GRID_TOP_MARGIN, 2)
        #         pygame.display.update()
        #         pygame.time.wait(3000)
        #         place_ships(computer_grid, SHIP_SIZES)
        #         start = True

    # if start:
    #     # if check_win():
    #     #     pass
    #     # else:
    #     # display_screen()
    #
    #     pygame.display.update()
    if not start:
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
        # row, col = generate_coords(GRID_SIZE)
        # result, is_killed = player_grid.shoot(row, col)
        turn += result

    game_over = display_screen()
