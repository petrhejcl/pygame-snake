from random import randint

from objects import *
from settings import *
from directions import *
from modes import BorderMode

class Game:
    def __init__(self, border_mode):
        self.game_map = None
        self.snake = None
        self.blank_squares_counter = None
        self.bounty = None
        self.score = None
        self.lost = None
        self.border_mode = border_mode
        # TODO: Implement
        self.id = None

    def reset_game(self):
        self.game_map = [[BLANK_OBJECT for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.blank_squares_counter = WIDTH * HEIGHT - STARTING_SNAKE_SIZE
        self.create_starting_snake()
        self.score = 0
        self.lost = False

        if self.border_mode is BorderMode.WALL:
            self.set_wall()

        self.generate_bounty()

    def set_wall(self):
        for x in range(WIDTH):
            self.game_map[0][x] = WALL_OBJECT
            self.game_map[HEIGHT - 1][x] = WALL_OBJECT

        for y in range(HEIGHT):
            self.game_map[y][0] = WALL_OBJECT
            self.game_map[y][WIDTH - 1] = WALL_OBJECT

        # -4 because Corners are common
        self.blank_squares_counter -= WIDTH * 2 + HEIGHT * 2 - 4

    def create_starting_snake(self):
        head = ((STARTING_X, STARTING_Y), EAST)
        body_1 = ((STARTING_X - 1, STARTING_Y), EAST)
        body_2 = ((STARTING_X - 2, STARTING_Y), EAST)

        self.game_map[STARTING_Y][STARTING_X] = SNAKE_OBJECT
        self.game_map[STARTING_Y][STARTING_X - 1] = SNAKE_OBJECT

        self.snake = [head, body_1, body_2]

    # TODO: Fix when bounty generates right after last square of snake it converts to snake
    # Should be fixed but has to be tested
    def generate_bounty(self):
        target_idx = randint(0, self.blank_squares_counter - 2)

        idx = 0

        print("Blank squares counter is ", self.blank_squares_counter)
        print("New bounty should be generated on idx ", target_idx)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                if idx == target_idx and self.game_map[y][x] == BLANK_OBJECT:
                    self.game_map[y][x] = BOUNTY_OBJECT
                    self.bounty = (x, y)
                    self.blank_squares_counter -= 1

                    print(f"Bounty generated at x: {x} y: {y}")
                    self.print_map()
                    return

                if self.game_map[y][x] == BLANK_OBJECT:
                    idx += 1

    def update_directions(self):
        for i in range(len(self.snake) - 1, 0, -1):
            rect, direction = self.snake[i]
            _, new_direction = self.snake[i - 1]
            self.snake[i] = (rect, new_direction)

    def extend_snake(self):
        last = self.snake[len(self.snake) - 1]
        last_position = last[0]
        last_direction = last[1]
        last_opposite_direction = (last_direction + 2) % 4

        new_x, new_y = move_one_position(last_position, last_opposite_direction)

        #TODO: Deduplicate
        if self.border_mode is BorderMode.TRANSIT:
            if new_x < 0 and last_direction == EAST:
                new_x = WIDTH - 1
            elif new_y < 0 and last_direction == SOUTH:
                new_y = HEIGHT - 1
            elif new_x >= WIDTH and last_direction == WEST:
                new_x = 0
            elif new_y >= HEIGHT and last_direction == NORTH:
                new_y = 0

        new_block = ((new_x, new_y), last_direction)
        self.game_map[new_y][new_x] = SNAKE_OBJECT
        self.snake.append(new_block)

    def update_snake(self):
        for i, (old_pos, direction) in enumerate(self.snake):
            old_x, old_y = old_pos
            new_pos = move_one_position(old_pos, direction)
            new_x, new_y = new_pos

            # TODO: Refactor, probably create function like: ".handle_border_collision" or so
            if self.border_mode is BorderMode.TRANSIT:
                if new_x >= WIDTH and direction == EAST:
                    new_x = 0
                elif new_y >= HEIGHT and direction == SOUTH:
                    new_y = 0
                elif new_x < 0 and direction == WEST:
                    new_x = WIDTH - 1
                elif new_y < 0 and direction == NORTH:
                    new_y = HEIGHT - 1

            self.snake[i] = ((new_x, new_y), direction)

            # TODO: Fix that wen snake collides with wall, it looks random
            if i == 0 and self.game_map[new_y][new_x] == SNAKE_OBJECT \
                    or self.game_map[new_y][new_x] == WALL_OBJECT:
                self.lost = True

                print(f"Lost with score {self.score}")
                self.print_map()
            elif self.game_map[new_y][new_x] == BOUNTY_OBJECT:
                print(f"Collided with bounty at x: {self.bounty[0]}, y: {self.bounty[1]}")

                self.score += 1
                self.extend_snake()
                self.generate_bounty()
            #else:
            self.game_map[old_y][old_x] = BLANK_OBJECT

            # If collides with wall, wall should be displayed
            if self.game_map[new_y][new_x] != WALL_OBJECT:
                self.game_map[new_y][new_x] = SNAKE_OBJECT

    def move_snake(self, new_direction):
        old_direction = self.snake[0][1]

        if new_direction is not None and \
            new_direction == (old_direction - 1) % 4 or \
                new_direction == (old_direction + 1) % 4:
            self.snake[0] = (self.snake[0][0], new_direction)

        self.update_snake()
        self.update_directions()

    def print_map(self):
        for y in range(HEIGHT):
            print(self.game_map[y])
