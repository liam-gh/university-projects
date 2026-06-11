# -----------------------------
#           IMPORTS
# -----------------------------

from kepoco import display
from utime import sleep_ms, ticks_ms
from sys import path
path.append("/Games/Othello_project")
from game_mechanics import initial_game_state, is_valid_move, apply_move, find_valid_positions, count_scores, print_game_state

# -----------------------------
#         PLAYER & AI
# -----------------------------    

"""
( ! ) Please do not toggle between black and white, as this will destabilise the game state.
The AI is to remain as white, and the player (You!) to remain black.
    
This is my fault, and something I will try and fix over the Christmas break.
"""

black_player = __import__("human")
white_player = __import__("lgh10_ai")
# white_player = __import__("ai_mark")

# -----------------------------
#         BOOT SCREEN
# -----------------------------

def boot_screen():

    """
    - Gives the player a short startup animation so it's clear the device has booted.
    - Centers the title and credit text roughly on the display.
    - Runs a quick flash loop (on / off) for a cool effect.
    """
   
    title = "OTHELLO"
    credit = "(login id redacted)"

    right_shift = -6 
    title_x = (display.width - len(title) * 4) // 2 + right_shift
    credit_x = (display.width - len(credit) * 4) // 2 + right_shift

    title_y = display.height // 4
    credit_y = title_y + 12

    flash_times = 4
    for _ in range(flash_times):
        display.fill(display.BLACK)
        display.drawText(title, title_x, title_y, display.LIGHTGRAY)
        display.drawText(credit, credit_x, credit_y, display.LIGHTGRAY)
        display.update()
        sleep_ms(500)

        display.fill(display.BLACK)
        display.update()
        sleep_ms(500)

# -----------------------------
#      DRAW GRID FUNCTION
# -----------------------------

def draw_grid(state, curr_player, potential_move, black_score, white_score):
   
    """
    - Paints the board background and the small cell grid.
    - Draws stones from "state" directly so the board view always matches the game state.
    - Shows valid moves and a potential move highlight on top of stones.
    - Updates the score counters on the display.
    """
    
    display.fill(display.BLACK)
    
    grid_size = 8
    cell_width = 6
    cell_height = 3
    total_width = grid_size * cell_width + (grid_size + 1)
    total_height = grid_size * cell_height + (grid_size + 1)
    offset_x = (display.width - total_width) // 2
    offset_y = 5

    valid_moves = find_valid_positions(state, curr_player) if curr_player else []

    for row in range(grid_size):
        for col in range(grid_size):
            x_start = offset_x + 1 + col * (cell_width + 1)
            y_start = offset_y + 1 + row * (cell_height + 1)

# Cell background
            for x in range(x_start, x_start + cell_width):
                for y in range(y_start, y_start + cell_height):
                    display.setPixel(x, y, display.DARKGRAY)

# Valid move marker
            if (col, row) in valid_moves:
                for x in range(x_start, x_start + cell_width):
                    for y in range(y_start, y_start + cell_height):
                        display.setPixel(x, y, display.LIGHTGRAY)

# Stones
            if state[row][col] == 'b':
                for x in range(x_start, x_start + cell_width):
                    for y in range(y_start, y_start + cell_height):
                        display.setPixel(x, y, display.BLACK)
            if state[row][col] == 'w':
                for x in range(x_start, x_start + cell_width):
                    for y in range(y_start, y_start + cell_height):
                        display.setPixel(x, y, display.WHITE)

# Potential move highlight
            if potential_move == (col, row):
                for x in range(x_start, x_start + cell_width):
                    for y in range(y_start, y_start + cell_height):
                        display.setPixel(x, y, display.BLACK)

# Inner grid lines
            for x in range(x_start - 1, x_start + cell_width + 1):
                display.setPixel(x, y_start - 1, display.BLACK)
                display.setPixel(x, y_start + cell_height, display.BLACK)
            for y in range(y_start - 1, y_start + cell_height + 1):
                display.setPixel(x_start - 1, y, display.BLACK)
                display.setPixel(x_start + cell_width, y, display.BLACK)

# Outer board outline
    for x in range(offset_x - 1, offset_x + total_width + 1):
        display.setPixel(x, offset_y - 1, display.LIGHTGRAY)
        display.setPixel(x, offset_y + total_height, display.LIGHTGRAY)
    for y in range(offset_y - 1, offset_y + total_height + 1):
        display.setPixel(offset_x - 1, y, display.LIGHTGRAY)
        display.setPixel(offset_x + total_width, y, display.LIGHTGRAY)

# Stone counters
    counter_y = max(offset_y - 4, 0)
    left_x = offset_x + 1
    right_x = offset_x + total_width - 2
    display.drawText(str(black_score), left_x, counter_y, display.WHITE)
    display.drawText(str(white_score), right_x, counter_y, display.WHITE)

    display.update()

# -----------------------------
#       SUPPORT FUNCTIONS
# -----------------------------

def recalculate_scores():
    
    """
    Update the black and white counters from the current game state.
    Kept small and direct so scores always match the board.
    """
    
    global white_score, black_score
    black_score, white_score = count_scores(game_state)

def show_potential_move(move, player):
   
    """
    Redraws the board to highlight potential move.
    """

    draw_grid(game_state, player, move, black_score, white_score)

# -----------------------------
#           MAIN
# -----------------------------

display.enableGrayscale()

# Initialise game state
game_state, black_score, white_score = initial_game_state()

# Show boot screen
boot_screen()

running = True
min_play_time = 100

while running:
    draw_grid(game_state, None, None, black_score, white_score)

    for c, colour, player in [("b", "Black", black_player), ("w", "White", white_player)]:
        s = ticks_ms()
        draw_grid(game_state, c, None, black_score, white_score)
        move = player.next_move(game_state, c, show_potential_move)
        e = ticks_ms()
        if e - s < min_play_time:
            sleep_ms(min_play_time - (e - s))

# No valid moves left for the player
        if not find_valid_positions(game_state, c):
            if black_score > white_score:
                outcome = "BLACK WINS!"
            elif white_score > black_score:
                outcome = "WHITE WINS!"
            else:
                outcome = "DRAW!"
            running = False
            break

        if move is None:

# Player conceded or ragequits (/s)
            running = False
            break

        if is_valid_move(move, c, game_state):
            game_state = apply_move(move, c, game_state)
            recalculate_scores()
        else:
            outcome = f"{colour} made illegal move ({move})!"
            running = False
            break

# -----------------------------
#      GAME OVER SEQUENCE
# -----------------------------

sleep_ms(1000)
display.fill(display.BLACK)
display.update()
sleep_ms(1000)

# GAME OVER text
text_x = (display.width - len("GAME OVER!") * 6) // 2
text_y = display.height // 3
display.drawText("GAME OVER!", text_x, text_y, display.WHITE)
display.update()
sleep_ms(1000)

# Outcome text
outcome_x = (display.width - len(outcome) * 6) // 2
outcome_y = text_y + 10
display.drawText(outcome, outcome_x, outcome_y, display.WHITE)
display.update()
sleep_ms(1000)

# Outcome blink anim
blink_time = 3000
end_time = ticks_ms() + blink_time
visible = True
while ticks_ms() < end_time:
    display.fill(display.BLACK)
    display.drawText("GAME OVER!", text_x, text_y, display.WHITE)
    if visible:
        display.drawText(outcome, outcome_x, outcome_y, display.WHITE)
    display.update()
    visible = not visible
    sleep_ms(300)

# Clear screen and final refresh
display.fill(display.BLACK)
display.update()
sleep_ms(1000)

# Print final state in shell
print()
print("Final Game State")
print_game_state(game_state)
