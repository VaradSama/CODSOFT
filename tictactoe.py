"""
============================================================
  Tic-Tac-Toe AI — Minimax Algorithm with Alpha-Beta Pruning
  Author : Varad | MCA – Cybersecurity, IIMS Chinchwad
  Language: Python 3.x
============================================================
"""

import random
import math
import os
import time

# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────
HUMAN = "X"   # Minimising player
AI    = "O"   # Maximising player
EMPTY = " "

WIN_SCORE  =  1
LOSS_SCORE = -1
DRAW_SCORE =  0

# Winning combinations (index pairs on a 1-D 9-cell board)
WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]

# ──────────────────────────────────────────────
# BOARD UTILITIES
# ──────────────────────────────────────────────

def create_board():
    """Return a fresh 3×3 board as a flat list of 9 cells."""
    return [EMPTY] * 9


def print_board(board):
    """Render the board with clear formatting to the terminal."""
    os.system("cls" if os.name == "nt" else "clear")
    print("\n  Tic-Tac-Toe — AI vs Human\n")
    print("   Position Guide:     Current Board:")
    rows = []
    for r in range(3):
        guide = f"   {r*3+1} | {r*3+2} | {r*3+3}    "
        cells = f"   {board[r*3]} | {board[r*3+1]} | {board[r*3+2]}"
        rows.append(guide + "    " + cells)
    separator = "  ---|---|---          ---|---|---"
    print(rows[0])
    print(separator)
    print(rows[1])
    print(separator)
    print(rows[2])
    print()


def get_empty_cells(board):
    """Return list of indices of empty cells."""
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def is_board_full(board):
    """Return True when no empty cells remain."""
    return len(get_empty_cells(board)) == 0


def check_winner(board, player):
    """Return True if *player* has achieved any winning combination."""
    for a, b, c in WIN_COMBOS:
        if board[a] == board[b] == board[c] == player:
            return True
    return False


def is_terminal(board):
    """Return True if the game is over (win or draw)."""
    return check_winner(board, AI) or check_winner(board, HUMAN) or is_board_full(board)


def evaluate(board):
    """
    Static evaluation function.
      AI wins  → +1
      Human wins → -1
      Draw / ongoing → 0
    """
    if check_winner(board, AI):
        return WIN_SCORE
    if check_winner(board, HUMAN):
        return LOSS_SCORE
    return DRAW_SCORE

# ──────────────────────────────────────────────
# MINIMAX WITH ALPHA-BETA PRUNING
# ──────────────────────────────────────────────

def minimax(board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    """
    Minimax algorithm with Alpha-Beta pruning.

    Parameters
    ----------
    board          : current game state (list of 9 cells)
    depth          : recursion depth (used for depth-limited search)
    is_maximizing  : True when it's the AI's (maximizer's) turn
    alpha          : best score the maximizer can guarantee so far
    beta           : best score the minimizer can guarantee so far

    Returns
    -------
    int : the best score achievable from this board state
    """
    # ── Base cases ──
    score = evaluate(board)
    if score != 0:          # Win / Loss detected
        return score
    if is_board_full(board): # Draw
        return DRAW_SCORE
    if depth == 0:           # Depth limit reached (Medium difficulty)
        return DRAW_SCORE

    empty_cells = get_empty_cells(board)

    if is_maximizing:
        # AI tries to MAXIMISE the score
        best = -math.inf
        for cell in empty_cells:
            board[cell] = AI                            # make move
            score = minimax(board, depth - 1, False, alpha, beta)
            board[cell] = EMPTY                         # undo move
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:                           # ── Prune ──
                break
        return best
    else:
        # Human tries to MINIMISE the score
        best = math.inf
        for cell in empty_cells:
            board[cell] = HUMAN                         # make move
            score = minimax(board, depth - 1, True, alpha, beta)
            board[cell] = EMPTY                         # undo move
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:                           # ── Prune ──
                break
        return best

# ──────────────────────────────────────────────
# AI MOVE SELECTION
# ──────────────────────────────────────────────

def get_ai_move(board, difficulty="hard"):
    """
    Choose the best move for the AI based on difficulty level.

    Difficulty Levels
    -----------------
    easy   → random move (no Minimax)
    medium → Minimax with depth limit = 3
    hard   → full Minimax (unbeatable)
    """
    empty_cells = get_empty_cells(board)

    if difficulty == "easy":
        # Random move — no strategy
        return random.choice(empty_cells)

    elif difficulty == "medium":
        # Minimax with limited depth (not always optimal)
        depth_limit = 3
    else:
        # Hard: full depth search — AI is unbeatable
        depth_limit = len(empty_cells)

    best_score = -math.inf
    best_move  = None

    for cell in empty_cells:
        board[cell] = AI                                     # try move
        score = minimax(board, depth_limit - 1, False)       # evaluate
        board[cell] = EMPTY                                  # undo move

        if score > best_score:
            best_score = score
            best_move  = cell

    return best_move

# ──────────────────────────────────────────────
# INPUT HELPERS
# ──────────────────────────────────────────────

def get_human_move(board):
    """
    Prompt the human player for a valid move (1–9).
    Validates input and ensures the chosen cell is empty.
    """
    while True:
        try:
            move = int(input("  Your move (1–9): ")) - 1   # convert to 0-indexed
            if move < 0 or move > 8:
                print("  ⚠ Enter a number between 1 and 9.")
            elif board[move] != EMPTY:
                print("  ⚠ That cell is already taken. Choose another.")
            else:
                return move
        except ValueError:
            print("  ⚠ Invalid input. Please enter a number.")


def get_difficulty():
    """Prompt the player to choose a difficulty level."""
    print("  Choose difficulty:")
    print("    1 → Easy   (random AI)")
    print("    2 → Medium (limited Minimax)")
    print("    3 → Hard   (full Minimax — unbeatable)\n")
    while True:
        choice = input("  Your choice (1/2/3): ").strip()
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "medium"
        elif choice == "3":
            return "hard"
        else:
            print("  ⚠ Enter 1, 2, or 3.")


def get_first_player():
    """Ask who moves first."""
    print("\n  Who moves first?")
    print("    1 → You (X)")
    print("    2 → AI  (O)\n")
    while True:
        choice = input("  Your choice (1/2): ").strip()
        if choice in ("1", "2"):
            return choice
        print("  ⚠ Enter 1 or 2.")

# ──────────────────────────────────────────────
# GAME LOOP
# ──────────────────────────────────────────────

def play_game():
    """Main game loop — handles one full match."""
    board      = create_board()
    difficulty = get_difficulty()
    first      = get_first_player()
    human_turn = (first == "1")      # True → human goes first

    print_board(board)

    while not is_terminal(board):
        if human_turn:
            # ── Human's turn ──
            print("  🧑 Your turn (X):")
            move = get_human_move(board)
            board[move] = HUMAN
        else:
            # ── AI's turn ──
            print("  🤖 AI is thinking…")
            time.sleep(0.4)          # brief pause for UX
            move = get_ai_move(board, difficulty)
            board[move] = AI
            print(f"  AI plays at position {move + 1}")
            time.sleep(0.3)

        print_board(board)
        human_turn = not human_turn  # swap turns

    # ── Game Over ──
    if check_winner(board, AI):
        print("  🤖 AI wins! Better luck next time.\n")
    elif check_winner(board, HUMAN):
        print("  🎉 You win! Congratulations!\n")
    else:
        print("  🤝 It's a draw! Well played!\n")


def main():
    """Entry point — allows multiple rounds."""
    os.system("cls" if os.name == "nt" else "clear")
    print("\n" + "="*50)
    print("   TIC-TAC-TOE  —  Minimax AI")
    print("   Developed by: Varad | MCA Cybersecurity")
    print("="*50 + "\n")

    while True:
        play_game()
        again = input("  Play again? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Thanks for playing! Goodbye.\n")
            break


if __name__ == "__main__":
    main()
