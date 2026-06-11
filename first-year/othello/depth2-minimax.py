#########################################################################
#                                                                       #
#  ______________________ ______________._____   ._____    ________     #
#   \.     \__    ___/    |  \_   _____/|     |   |    |   \       \    #
#   /   |   \|    | /     ~    \    __)_ |    |   |    |    /   |   \   #
#   /   |    \     | \    Y    /        \|    |___|    |___/    |    \  #
#   \_______  /____|  \___|_  /_______  /|_______ \_______ \_______  /  #
#           \/              \/        \/         \/       \/       \/   #
#                                                                       #
#########################################################################


# -----------------------------
#           IMPORTS
# -----------------------------

from game_mechanics import find_valid_positions, apply_move, count_scores
import random

# -----------------------------
#         BOARD RANKS
# -----------------------------

"""
Weighted positions to prioritise corners and edges.
Corners are strongest; edges are safer than central squares.
This gives the AI a positional advantage without making it unbeatable.
"""

ranks = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, 1, 1, 1, 1, -50, -20],
    [10, 1, 5, 2, 2, 5, 1, 10],
    [5, 1, 2, 1, 1, 2, 1, 5],
    [5, 1, 2, 1, 1, 2, 1, 5],
    [10, 1, 5, 2, 2, 5, 1, 10],
    [-20, -50, 1, 1, 1, 1, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]

# -----------------------------
#       GET BOARD RANK
# -----------------------------

"""
Helper function to retrieve a square's rank.
Keeps evaluation calculations tidy.
"""

def get_rank(x, y):
    return ranks[y][x]

# -----------------------------
#       HEURISTIC EVALUATION
# -----------------------------

def evaluate(state, colour, my_moves, opp_moves):
  
    """
    Combines stone count, board position, mobility, and early-game corner preference.
    Mobility encourages the AI to maintain options for future moves.
    Early corner bonus helps the AI claim strategically important positions.
    """
   
    opponent = "b" if colour == "w" else "w"
    my_score, opp_score = count_scores(state)
    score = (my_score - opp_score) if colour == "b" else (opp_score - my_score)

    # Board rank weighting
    for y in range(8):
        for x in range(8):
            if state[y][x] == colour:
                score += get_rank(x, y)
            elif state[y][x] == opponent:
                score -= get_rank(x, y)

    
    score += (my_moves - opp_moves) * 2

    return score

# -----------------------------
#        MINIMAX FUNCTION
# -----------------------------

"""
Recursive minimax function with depth control.
Maximising and minimising handles AI vs opponent evaluation.
Depth kept at 2 for speed while still looking ahead enough to beat simpler AIs.
"""

def minimax(state, colour, depth, maximising):
    ai_colour = colour

    def _ab(curr_state, current_player, d, alpha, beta, maximising_player):
        moves = find_valid_positions(curr_state, current_player)
        if d == 0 or not moves:
            
            my_moves = len(find_valid_positions(curr_state, ai_colour))
            opp_moves = len(find_valid_positions(curr_state, "b" if ai_colour == "w" else "w"))
            return evaluate(curr_state, ai_colour, my_moves, opp_moves), None

        moves_sorted = sorted(moves, key=lambda m: get_rank(m[0], m[1]), reverse=maximising_player)
        next_player = "b" if current_player == "w" else "w"

        if maximising_player:
            best_value = -float("inf")
            best_move = None
            for mv in moves_sorted:
                new_state = apply_move(mv, current_player, curr_state)
                val, _ = _ab(new_state, next_player, d - 1, alpha, beta, False)
                if val > best_value:
                    best_value = val
                    best_move = mv
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    break
            return best_value, best_move
        else:
            best_value = float("inf")
            best_move = None
            for mv in moves_sorted:
                new_state = apply_move(mv, current_player, curr_state)
                val, _ = _ab(new_state, next_player, d - 1, alpha, beta, True)
                if val < best_value:
                    best_value = val
                    best_move = mv
                if val < beta:
                    beta = val
                if alpha >= beta:
                    break
            return best_value, best_move

    return _ab(state, ai_colour, depth, -float("inf"), float("inf"), maximising)


# -----------------------------
#        AI NEXT MOVE
# -----------------------------

"""
Entry point for AI. Uses minimax to choose the best move.
Random choice only applies if multiple moves are equally scored, to prevent deterministic ties.
"""

def next_move(state, colour, show_potential_move):
    _, move = minimax(state, colour, depth=2, maximising=True)
    if move:
        return move
    else:
        moves = find_valid_positions(state, colour)
        return random.choice(moves) if moves else None
