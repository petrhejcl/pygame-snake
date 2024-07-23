import pygame

EAST, SOUTH, WEST, NORTH = 0, 1, 2, 3
KEYS_TO_DIRECTIONS = {pygame.K_RIGHT : EAST,
                      pygame.K_DOWN : SOUTH,
                      pygame.K_LEFT : WEST,
                      pygame.K_UP : NORTH}


def move_one_position(initial_position, direction):
    old_x, old_y = initial_position

    if direction == EAST:
        return old_x + 1, old_y
    elif direction == SOUTH:
        return old_x, old_y + 1
    elif direction == WEST:
        return old_x - 1, old_y
    else:
        return old_x, old_y - 1
