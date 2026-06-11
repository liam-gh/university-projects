from game_mechanics import is_valid_state, is_valid_move, is_empty, is_player, is_opponent, find_valid_positions

from random import choice

# The entry point for the player. The game calls this when it is this players turn to
# make a move. The player is provided the game state, the colour of their stones, and
# a function to draw a potential move to the screen (it takes a single coordinate pair
# and the player colour. This is useful to human players to show the currently selected
# move andfor debugging AI). This function should return a cooridinate pair for the 
# move it wants to play, or None to concede the game.
def next_move(state, color, show_potential_move):
    moves = find_valid_positions(state, color)
    if moves:
        return choice(moves)
    else:
        return None