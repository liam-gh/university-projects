_scan_directions = [
    ( 1, 0),
    ( 0, 1),
    (-1, 0),
    ( 0,-1),
    ( 1, 1),
    (-1,-1),
    ( 1,-1),
    (-1, 1),
]

# Returns the initial state of the game in Othello, along with the initial scores for each player.
def initial_game_state():
    state = [[None]*8 for _ in range(8)]
    state[4][4] = state[3][3] = "b"
    state[4][3] = state[3][4] = "w"
    return state, 2, 2

# Checks if the there is no stone at a given location.
def is_empty(location: tuple[int, int], state: list[list[str]]) -> bool:
    return state[location[1]][location[0]] is None

# Checks if the player has a stone at a given location.
def is_player(location: tuple[int, int], player: str, state: list[list[str]]) -> bool:
    return state[location[1]][location[0]] == player

# Checks if the players opponent has a stone at a given location.
def is_opponent(location, player, state):
    return state[location[1]][location[0]] and state[location[1]][location[0]] != player

# Checks if the game state is valid.
def is_valid_state(state):
    if len(state) != 8:
        return False
    for i in range(3):
        if len(state[i]) != 8:
            return False
    for y in range(8):
        for x in range(8):
            if state[y][x] is not None and state[y][x] not in ["b", "w"]:
                return False
    return True

# Checks if a given move by a player is valid for the specified game state.
def is_valid_move(move, player, state):
    if (type(move) is tuple) and (len(move) == 2) and (move[0] in range(8)) and (move[1] in range(8)) and (state[move[1]][move[0]] is None):
        ox, oy = move
        for dx, dy in _scan_directions:
            tx, ty = ox+dx, oy+dy
            if (tx in range(8)) and (ty in range(8)) and is_opponent((tx,ty), player, state):
                tx += dx
                ty += dy
                while (tx in range(8)) and (ty in range(8)) and is_opponent((tx,ty), player, state):
                    tx += dx
                    ty += dy
                if (tx in range(8)) and (ty in range(8)) and is_player((tx,ty), player, state):
                    return True
    else:
        return False

# Create a new game state with the specified move applied for the requested
# player. Does NOT modify the original game state.
def apply_move(move, player, state):
    ox, oy = move
    
    state = [list(row) for row in state] # clone the previous game state
    
    for dx, dy in _scan_directions:
        tx, ty = ox+dx, oy+dy
        if (tx in range(8)) and (ty in range(8)) and is_opponent((tx,ty), player, state):
            tx += dx
            ty += dy
            c = 2
            while (tx in range(8)) and (ty in range(8)) and is_opponent((tx,ty), player, state):
                tx += dx
                ty += dy
                c += 1
            if (tx in range(8)) and (ty in range(8)) and is_player((tx,ty), player, state):
                for i in range(c):
                    state[oy + dy*i][ox + dx*i] = player
    return state

# Takes a given state and a player ("b", or "w") and returns a list of
# coordinate pairs of all the valid moves.
def find_valid_positions(state, player):
    pos = []
    for y in range(8):
        for x in range(8):
            if is_valid_move((x,y), player, state):
                pos.append((x, y))
    return pos

# Takes a given game state and counts how many stones each play has.
# The scores are returned as the pair (black score, white score)
def count_scores(state):
    black_score = white_score = 0
    for y in range(8):
        for x in range(8):
            if state[y][x] == "b":
                black_score += 1
            elif state[y][x] == "w":
                white_score += 1
    return black_score, white_score


# A useful debugging function that prints a given game state to the terminal/shell
# Can also accept an optional list of potential moves as a list of coordinate pairs.
def print_game_state(state, potential_moves = None):
    if potential_moves is None:
        potential_moves = []
    
    lines = [" ".join([("?" if (x,y) in potential_moves else ".") if cell is None else cell for x, cell in enumerate(row)]) for y, row in enumerate(state)]
    
    print("+---------------+")
    for line in lines:
        print(f"|{line}|")
    print("+---------------+")
