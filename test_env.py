#!/usr/bin/env python3

from battlesnake_env import env
from survival_utils import wall_collision, self_collision, other_snakes_collision

import random

def agent_get_action(state):
    data = state
    board_data = data["board"]
    board_ht = board_data["height"]
    board_wth = board_data["width"]

    you_data = data["you"]
    you_head = you_data["head"]
    you_body = you_data["body"]
    you_id = you_data["id"]

    other_snakes_body = [snake["body"] for snake in board_data["snakes"]
                         if snake["id"] != you_id]

    possible_moves = ["up", "down", "left", "right"]
    safe_from_collision = [move
                           for move in possible_moves
                           if (not wall_collision(move, you_head, board_wth, board_ht) and
                               not self_collision(move, you_body, you_head) and
                               not other_snakes_collision(move, other_snakes_body, you_head))]

    if len(safe_from_collision) == 0:
        print("no safe move, DIE")
        return {"move": "up"}

    move = random.choice(safe_from_collision)
    return move

for i_episode in range(1):
    print("Episode:", i_episode)
    done = False
    initial_state = env.reset(train_mode=True)
    score = 0
    t = 0

    state, _reward, done = initial_state
    print(state)
    while not done:
        t += 1
        print("step:", i_episode, t)
        action = agent_get_action(state)
        next_state, reward, done = env.step(action)
        state = next_state
        print(state)
        # agent.step(state, action, reward, next_state, done)
        score += reward
        #print("app:", next_state, action, reward, done)
        print(t, "app:", action, reward, done)

print("app: done")
env.close()

