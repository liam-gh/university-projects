from game_mechanics import is_valid_state, is_valid_move, is_empty, is_player, is_opponent, find_valid_positions, count_scores, apply_move
from thumbyButton import buttonU, buttonD, buttonL, buttonR, buttonA, buttonB
from utime import sleep_ms

buttons = {
    "a": buttonA,
    "b": buttonB,
    "u": buttonU,
    "d": buttonD,
    "l": buttonL,
    "r": buttonR,
}

def find_valid_cursor(state):
    moves = find_valid_positions(state, "b")
    if moves:
        return moves[0]
    else:
        return None

def await_button_press():
    while True:
        for k, b in buttons.items():
            if b.justPressed():
                return k
        sleep_ms(50)

def move_vertical(cursor, dir, state):
    for dy in map(lambda x: x*dir, range(1,8)):
        y = (cursor[1] + dy) % 8
        for dx in [0, -1, 1, -2, 2, -3, 3, -4]:
            x = (cursor[0] + dx) % 8
            if is_valid_move((x,y), "b", state):
                return x, y
    return cursor

def move_horizontal(cursor, dir, state):
    for dx in map(lambda x: x*dir, range(1,8)):
        x = (cursor[0] + dx) % 8
        for dy in [0, -1, 1, -2, 2, -3, 3, -4]:
            y = (cursor[1] + dy) % 8
            if is_valid_move((x,y), "b", state):
                return x, y
    return cursor

# The entry point for the player. The game calls this when it is this players turn to
# make a move. The player is provided the game state, the colour of their stones, and
# a function to draw a potential move to the screen (it takes a single coordinate pair
# and the player colour. This is useful to human players to show the currently selected
# move andfor debugging AI). This function should return a cooridinate pair for the 
# move it wants to play, or None to concede the game.
def next_move(state, colour, show_potential_move):
    
    moves = find_valid_positions(state, "b")
    if moves:
        cursor = moves[0]
    else:
        return None # no moves left
    
    while True:
        show_potential_move(cursor, colour)
        
        pressed = await_button_press()
        if pressed == "a":
            return cursor # play move
        elif pressed == "u":
            cursor = move_vertical(cursor, -1, state)
        elif pressed == "d":
            cursor = move_vertical(cursor, 1, state)
        elif pressed == "l":
            cursor = move_horizontal(cursor, -1, state)
        elif pressed == "r":
            cursor = move_horizontal(cursor, 1, state)
        elif pressed == "b":
            return None # concede game
