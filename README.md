# Tic-Tac-Toe AI — Minimax Algorithm with Alpha-Beta Pruning

**Developer:** Varad | MCA – Cybersecurity | IIMS Chinchwad, Pune  
**Language:** Python 3.x + HTML/CSS/JavaScript  
**Algorithm:** Minimax with Alpha-Beta Pruning

---

## Project Structure

```
tictactoe/
├── tictactoe.py          # Python CLI game (Minimax AI)
├── test_tictactoe.py     # 14 unit tests
├── index.html            # Web-based GUI 
└── README.md             # This file
```

---

## Quick Start

### Python CLI Version
```bash
python tictactoe.py
```

### Run Tests
```bash
python test_tictactoe.py
```

### Web Version
Open `index.html` in any modern browser — no server needed.

---

## How It Works

1. The AI uses **Minimax** — a recursive algorithm that explores all possible future moves.
2. **Alpha-Beta pruning** eliminates branches that cannot affect the outcome, reducing evaluations by ~50%.
3. Three difficulty levels: **Easy** (random), **Medium** (depth-3 Minimax), **Hard** (full Minimax — unbeatable).

---

## Scoring
| Outcome | Score |
|---------|-------|
| AI wins | +1    |
| Human wins | -1 |
| Draw | 0     |

---

## Key Functions

| Function | Purpose |
|----------|---------|
| `minimax()` | Core recursive AI logic with Alpha-Beta pruning |
| `get_ai_move()` | Selects best move based on difficulty |
| `check_winner()` | Detects all 8 winning combinations |
| `evaluate()` | Returns terminal state score |
| `get_human_move()` | Validates and reads player input |

---


