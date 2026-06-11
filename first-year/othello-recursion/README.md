<div align="center">

![readme-image](README.png)

# Othello - Recursive Minimax Algorithm
Depth-2 Recursive Minimax Algorithm Implementation & Visual Improvements to the classic boardgame "Othello" (aka. Reversi).

</div>

<div align="center">

![Date](https://img.shields.io/badge/Date-5th%20December%202025-blue)

</div>

<div align="center">

![Language](https://img.shields.io/badge/Language-Micro%20Python-red)
![Module](https://img.shields.io/badge/Module-Programming%20I-orange)
![Grade](https://img.shields.io/badge/Grade-65%25-green)

</div>

---


## Overview

In this project, I implemented a depth-2 minimax AI that reliably outperforms both ai_mark and ai_random.

The AI uses a depth-2 minimax algorithm, consistently outperforming both ai_mark and ai_random. I opted for an 8×8 board rather than the simpler 4×4 grid — this opens up more strategic complexity, particularly around edge and corner control, and gives the AI richer positions to evaluate.
The current depth is intentional. An earlier version ran deeper searches but introduced noticeable lag between moves. Depth-2 strikes a better balance between responsiveness and decision quality, though it does mean some deeper strategies won't always be found.


Beyond the game logic, I put significant work into the interface:

* Boot screen on launch
* Multiple distinct outcome screens (win, loss, draw)
* Custom board
* Visual feedback for stone counters and move highlight indicators

---


## Important Context (Grade / Feedback)

Initially, I created a depth-5 algorithm, meaning the AI checks 4 moves in advance, though due to hardware constraints I dialled it back significantly.
Unbeknownst to me, the "testing" would not be done on the actual KePoCo hardware, though via an automated grading script/program.

This means that my efforts to downgrade the complexity of the program actually resulted in a lower grade. 
This was made clear to me through an email conversation I had with my lecturer upon submission.

My final grade for this assignment resulted in 65% due to this.

---


## Scripts / Files  

| Script | Purpose |
|--------|---------|
| `depth2-minimax.py` | My AI, which features a depth-2 minimax algorithm |
| `othello.py` | Entry point (main game script) |
| `game_mechanics.py`| Handles the base game mechanics |
| `human.py` | Handles the player's input |
| `~/ai`| Example AI's provided by UKC | 

---

## How it Works

* Uses a weighted board (ranks) that favours corners and edges.
* Evaluates moves based on stone count, board position, and mobility.
* Depth-2 minimax looks ahead one opponent response, choosing moves that maximise advantage.
* Falls back to a random legal move if no minimax move is available.
* Designed to be lightweight enough for smooth gameplay on typical devices.

---

## What I Would've Done Next Time
- [ ] Kept original depth-5 algorithm
- [ ] Less focus on visual improvements
