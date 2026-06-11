from game_mechanics import is_valid_state, is_valid_move, is_empty, is_player, is_opponent, find_valid_positions, count_scores, apply_move, print_game_state

from random import choice

ranks = [
    [5,0,4,1],
    [0,0,3,2],
    [4,3,4,1],
    [1,2,1,0],
]

def rank(x, y):
    if x >= 4:
        x = 7-x
    if y >= 4:
        y = 7-y
    return ranks[x][y]

# The entry point for the player. The game calls this when it is this players turn to
# make a move. The player is provided the game state, the colour of their stones, and
# a function to draw a potential move to the screen (it takes a single coordinate pair
# and the player colour. This is useful to human players to show the currently selected
# move andfor debugging AI). This function should return a cooridinate pair for the 
# move it wants to play, or None to concede the game.
def next_move(state, colour, show_potential_move):
    moves = find_valid_positions(state, colour)
    if moves:
        
        # print_game_state(state, moves) # useful for debugging
        
        ranked = list(sorted((rank(*m), m) for m in moves))
        best = [m for r, m in ranked if r == ranked[-1][0]]
        if len(best) > 1:
            return sorted([(count_scores(apply_move(m, colour, state))[0 if colour == "b" else 1], m) for m in best])[-1][1]
        else:
            return best[0]
    else:
        return None