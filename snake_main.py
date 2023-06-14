import argparse
import game_utils
from snake_game import SnakeGame
from game_display import GameDisplay
from snake import *

def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:
    # INIT OBJECTS
    game = SnakeGame(args)
    gd.show_score(0)
    if game.get_walls_num() > 0:
        game.add_wall()
    if game.get_num_apples() > 0:
        game.add_apple()

    # DRAW BOARD
    game.draw_board(gd)
    game.end_round()
    gd.end_round()
    # END OF ROUND 0
    while not game.is_over():
        # CHECK KEY CLICKS
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        # UPDATE OBJECTS
        game.update_objects()
        # DRAW BOARD
        game.draw_board(gd)
        # WAIT FOR NEXT ROUND:
        game_score = game.get_score()
        gd.show_score(game_score)
        game.end_round()
        gd.end_round()

