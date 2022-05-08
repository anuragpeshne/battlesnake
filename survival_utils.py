#!/usr/bin/env python3

def wall_collision(move, head, board_wth, board_ht):
    hx, hy = head['x'], head['y']
    if ((move == "down" and (hy - 1 >= 0)) or
        (move == "right" and (hx + 1 <= board_wth - 1)) or
        (move == "up" and (hy + 1 <= board_ht - 1)) or
        (move == "left" and (hx - 1 >= 0))):
        return False
    else:
        return True


def self_collision(move, body, head):
    body_coord_tuples = [(cell['x'], cell['y']) for cell in body]
    body_set = set(body_coord_tuples)

    if move == "down":
        new_head_tuple = (head['x'], head['y'] - 1)
    elif move == "right":
        new_head_tuple = (head['x'] + 1, head['y'])
    if move == "up":
        new_head_tuple = (head['x'], head['y'] + 1)
    if move == "left":
        new_head_tuple = (head['x'] - 1, head['y'])

    return new_head_tuple in body_set
