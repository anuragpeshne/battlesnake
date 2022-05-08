#!/usr/bin/env python3

import logging
import os
import random

from flask import Flask
from flask import request

from survival_utils import wall_collision, self_collision, other_snakes_collision

app = Flask(__name__)

@app.get("/")
def handle_info():
    """
    This function is called when the snake is registered.
    See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake
    """
    print("INFO")
    return {
        "apiversion": "1",
        "author": "Anurag Peshne",
        "color": "#fbdd74",
        "head": "beluga",
        "tail": "curled"
    }

@app.post("/start")
def handle_start():
    """
    This function is called everytime the snake is entered into a game.
    request.json contains information about the game that's about to be played.
    """
    data = request.get_json()

    print(data)
    print(f"{data['game']['id']} START")
    return "ok"

@app.post("/move")
def handle_move():
    """
    This function is called on every turn of a game.
    Return a move from ["up", "down", "left" or "right"].
    """
    data = request.get_json()

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
    print(board_ht, board_wth, you_head, move, safe_from_collision)

    return {"move": move}


@app.post("/end")
def end():
    """
    This function is called when a game your snake was in ends.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = request.get_json()

    print(f"{data['game']['id']} END")
    return "ok"


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    port = int(os.environ.get("PORT", "8080"))
    print(f"Starting Battlesnake Server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
