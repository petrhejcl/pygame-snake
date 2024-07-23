import pygame
from colors import *
from modes import BorderMode
from settings import *
from directions import *
from game import Game
from objects import *

pygame.font.init()

def initial_window_setup():
    win = pygame.display.set_mode(RES)
    pygame.display.set_caption("Snake")
    return win


def new_direction_from_key_pressed():
    keys = pygame.key.get_pressed()

    for key in KEYS_TO_DIRECTIONS:
        if keys[key]:
            return KEYS_TO_DIRECTIONS[key]

    return None


def draw_score(win, score):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(score), True, MID_GREY)
    text_rect = text.get_rect()
    win.blit(text, text_rect)


def draw_lost(win, score):
    lost_font = pygame.font.Font('freesansbold.ttf', 60)
    lost_text = lost_font.render("You lost", True, MID_GREY)
    lost_rect = lost_text.get_rect()
    lost_rect.center = (WIDTH * SQUARE // 2, HEIGHT * SQUARE // 2)

    #score_font = pygame.font.Font('freesansbold.ttf', 24)
    #score_text = score_font.render(f"Your score is {score}", True, DARK_GREY)

    win.blit(lost_text, lost_rect)


# Debugging function
def draw_grid(win, game):
    font = pygame.font.Font('freesansbold.ttf', 20)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            text = font.render(str(game.game_map[y][x]), True, MID_GREY)
            _, _, w, h = text.get_rect()
            rect = (x * SQUARE, y * SQUARE, w, h)
            win.blit(text, rect)

def draw_snake(win, x, y):
    snake_rect = (x * SQUARE, y * SQUARE, SNAKE, SNAKE)
    pygame.draw.rect(win, BLACK, snake_rect)


def draw_wall(win, x, y):
    rect = (x * SQUARE, y * SQUARE, SQUARE, SQUARE)
    pygame.draw.rect(win, BLACK, rect)


def draw_bounty(win, x, y):
    bounty_rect = (x * SQUARE, y * SQUARE, SNAKE, SNAKE)
    pygame.draw.rect(win, RED, bounty_rect)


# TODO: This is probably too slow
def draw_map(win, game):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            tile = game.game_map[y][x]

            if tile == WALL_OBJECT:
                draw_wall(win, x, y)

            elif tile == SNAKE_OBJECT:
                draw_snake(win, x, y)

            elif tile == BOUNTY_OBJECT:
                draw_bounty(win, x, y)


def draw_window(win, game):
    win.fill(WHITE)

    draw_score(win, game.score)
    draw_map(win, game)

    #draw_grid(win, game)

    if game.lost:
        draw_lost(win, game.score)

    pygame.display.update()


def waiting_for_reset(game):
    waiting_for_input = True

    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.reset_game()
                waiting_for_input = False
                return True


def draw_menu_items(win, items):
    menu_item_font = pygame.font.Font('freesansbold.ttf', 60)

    for item in items:
        text, active = item

        item_text = menu_item_font.render(text, True, MID_GREY)
        lost_rect = item_text.get_rect()
        lost_rect.center = (WIDTH * SQUARE // 2, HEIGHT * SQUARE // 2)


def draw_main_menu(win):
    border_mode = ("Border Mode", True)
    borderless_mode = ("Borderless Mode", False)

    options = [border_mode, borderless_mode]




# TODO:
# 1) Add suport for walls and custom maps
# 2) Create logging (keys pressed, position at each time, game id etc.)
def main():
    win = initial_window_setup()
    clock = pygame.time.Clock()
    run = True

    game = Game(BorderMode.TRANSIT)

    game.reset_game()
    #game.set_wall()

    timer = 0

    new_direction = None

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        new_direction_tmp = new_direction_from_key_pressed()

        # Debugging
        if pygame.key.get_pressed()[pygame.K_LCTRL]:
            print("Game when score is: ", game.score)
            game.print_map()

        if new_direction_tmp is not None:
            new_direction = new_direction_tmp

        if timer == TIME_BORDER:
            timer = 0
            game.move_snake(new_direction)

        draw_window(win, game)

        if game.lost:
            run = waiting_for_reset(game)
            print("Game resetted")
            print(f"Direction of snake should be {game.snake[0][1]}")
            draw_window(win, game)
            pygame.event.clear()

        timer += 1


if __name__ == "__main__":
    main()
