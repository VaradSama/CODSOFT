/**
 * ═══════════════════════════════════════════════════════════
 *  NEXUS — Tic-Tac-Toe AI  |  script.js
 *  Core Logic: Minimax + Alpha-Beta Pruning (unchanged)
 *  UI Layer: Premium interactions, animations, state machine
 * ═══════════════════════════════════════════════════════════
 */

'use strict';

/* ────────────────────────────────────────────────────────────
   1. CONSTANTS & CONFIGURATION
   ──────────────────────────────────────────────────────────── */

/** All eight winning combinations (indices on 0–8 flat board) */
const WIN_COMBOS = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],   // rows
  [0, 3, 6], [1, 4, 7], [2, 5, 8],   // columns
  [0, 4, 8], [2, 4, 6],              // diagonals
];

/** Scoring constants for the evaluation function */
const SCORE = { WIN: 1, LOSS: -1, DRAW: 0 };

/** AI "thinking" delay in ms — makes it feel realistic */
const AI_DELAY = 420;

/* SVG coordinates for drawing the animated win line.
   Each entry maps to a WIN_COMBO index (0–7):
   [x1%, y1%, x2%, y2%] as fractions of the board size */
const WIN_LINE_COORDS = [
  [0.17, 0.17, 0.83, 0.17],  // row 0  (top)
  [0.17, 0.50, 0.83, 0.50],  // row 1  (mid)
  [0.17, 0.83, 0.83, 0.83],  // row 2  (bot)
  [0.17, 0.17, 0.17, 0.83],  // col 0  (left)
  [0.50, 0.17, 0.50, 0.83],  // col 1  (mid)
  [0.83, 0.17, 0.83, 0.83],  // col 2  (right)
  [0.17, 0.17, 0.83, 0.83],  // diag 0 (TL→BR)
  [0.83, 0.17, 0.17, 0.83],  // diag 1 (TR→BL)
];

/* ────────────────────────────────────────────────────────────
   2. MINIMAX ALGORITHM WITH ALPHA-BETA PRUNING
   ──────────────────────────────────────────────────────────── */

/**
 * Returns indices of all empty cells on the board.
 * @param {Array<string|null>} board
 * @returns {number[]}
 */
function emptyCells(board) {
  return board.reduce((acc, v, i) => { if (!v) acc.push(i); return acc; }, []);
}

/**
 * Returns true if the given player has won.
 * @param {Array<string|null>} board
 * @param {string} player  'X' or 'O'
 * @returns {boolean}
 */
function hasWon(board, player) {
  return WIN_COMBOS.some(([a, b, c]) =>
    board[a] === player && board[b] === player && board[c] === player
  );
}

/**
 * Returns the winning combo array for a player, or null.
 * @param {Array<string|null>} board
 * @param {string} player
 * @returns {number[]|null}
 */
function getWinningCombo(board, player) {
  return WIN_COMBOS.find(([a, b, c]) =>
    board[a] === player && board[b] === player && board[c] === player
  ) ?? null;
}

/**
 * Static evaluation of a terminal board state.
 * @param {Array<string|null>} board
 * @param {string} ai    AI symbol
 * @param {string} human Human symbol
 * @returns {number} +1 (AI wins), -1 (Human wins), 0 (draw)
 */
function evaluate(board, ai, human) {
  if (hasWon(board, ai))    return SCORE.WIN;
  if (hasWon(board, human)) return SCORE.LOSS;
  return SCORE.DRAW;
}

/**
 * Minimax with Alpha-Beta pruning.
 *
 * @param {Array<string|null>} board        - Current board state
 * @param {number}             depth        - Remaining search depth
 * @param {boolean}            isMaximizing - true = AI's turn
 * @param {number}             alpha        - Best score maximiser can guarantee
 * @param {number}             beta         - Best score minimiser can guarantee
 * @param {string}             ai           - AI symbol
 * @param {string}             human        - Human symbol
 * @returns {number} The best achievable score from this position
 */
function minimax(board, depth, isMaximizing, alpha, beta, ai, human) {
  // ── Base cases ──────────────────────────────────────────
  const score = evaluate(board, ai, human);
  if (score !== 0)               return score;        // Terminal win/loss

  const empty = emptyCells(board);
  if (empty.length === 0 || depth === 0) return SCORE.DRAW; // Draw or depth limit

  if (isMaximizing) {
    // AI tries to MAXIMISE the score
    let best = -Infinity;
    for (const idx of empty) {
      board[idx] = ai;                                         // Try move
      const s = minimax(board, depth - 1, false, alpha, beta, ai, human);
      board[idx] = null;                                       // Undo move
      best  = Math.max(best, s);
      alpha = Math.max(alpha, best);
      if (beta <= alpha) break;                               // ── PRUNE ──
    }
    return best;
  } else {
    // Human tries to MINIMISE the score
    let best = Infinity;
    for (const idx of empty) {
      board[idx] = human;                                      // Try move
      const s = minimax(board, depth - 1, true, alpha, beta, ai, human);
      board[idx] = null;                                       // Undo move
      best = Math.min(best, s);
      beta = Math.min(beta, best);
      if (beta <= alpha) break;                               // ── PRUNE ──
    }
    return best;
  }
}

/**
 * Select the best move for the AI based on difficulty.
 *
 * @param {Array<string|null>} board
 * @param {string}             ai
 * @param {string}             human
 * @param {'easy'|'medium'|'hard'} difficulty
 * @returns {number} Cell index to play
 */
function getBestMove(board, ai, human, difficulty) {
  const empty = emptyCells(board);
  if (!empty.length) return -1;

  // Easy: completely random — no intelligence
  if (difficulty === 'easy') {
    return empty[Math.floor(Math.random() * empty.length)];
  }

  // Medium: depth-limited minimax (not always optimal)
  // Hard:   full depth minimax (unbeatable)
  const depthLimit = difficulty === 'medium' ? 3 : empty.length;

  let bestScore = -Infinity;
  let bestMove  = empty[0];

  for (const idx of empty) {
    board[idx] = ai;
    const score = minimax(board, depthLimit - 1, false, -Infinity, Infinity, ai, human);
    board[idx] = null;
    if (score > bestScore) {
      bestScore = score;
      bestMove  = idx;
    }
  }

  return bestMove;
}

/* ────────────────────────────────────────────────────────────
   3. DOM REFERENCES
   ──────────────────────────────────────────────────────────── */

const $ = (id) => document.getElementById(id);

const dom = {
  board:          $('board'),
  statusPanel:    $('statusPanel'),
  statusDot:      $('statusDot'),
  pulseRing:      $('pulseRing'),
  statusMain:     $('statusMain'),
  statusHint:     $('statusHint'),
  modeLabel:      $('modeLabel'),
  scoreHuman:     $('score-human'),
  scoreAI:        $('score-ai'),
  scoreDraw:      $('score-draw'),
  barHuman:       $('bar-human'),
  barAI:          $('bar-ai'),
  barDraw:        $('bar-draw'),
  humanLabel:     $('humanLabel'),
  aiLabel:        $('aiLabel'),
  restartBtn:     $('restartBtn'),
  resetScoreBtn:  $('resetScoreBtn'),
  difficultyEl:   $('difficulty'),
  winLineSvg:     $('winLineSvg'),
  winLine:        $('winLine'),
  btnX:           $('btn-X'),
  btnO:           $('btn-O'),
};

/* ────────────────────────────────────────────────────────────
   4. GAME STATE
   ──────────────────────────────────────────────────────────── */

let state = {
  board:      Array(9).fill(null),
  humanSym:   'X',
  aiSym:      'O',
  isAiTurn:   false,        // human goes first by default (X)
  gameOver:   false,
  thinkTimer: null,
  score: { human: 0, ai: 0, draw: 0 },
};

/* ────────────────────────────────────────────────────────────
   5. CELL SVG MARKS
   ──────────────────────────────────────────────────────────── */

/**
 * Returns an SVG element for X or O to render inside a cell.
 * Using inline SVG ensures crisp rendering at all sizes.
 */
function createMark(symbol) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 40 40');
  svg.setAttribute('fill', 'none');
  svg.setAttribute('stroke', 'currentColor');
  svg.setAttribute('stroke-width', '3.2');
  svg.setAttribute('stroke-linecap', 'round');
  svg.classList.add('cell-mark');
  svg.setAttribute('aria-hidden', 'true');

  if (symbol === 'X') {
    // Two diagonal lines
    const l1 = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    l1.setAttribute('x1', '10'); l1.setAttribute('y1', '10');
    l1.setAttribute('x2', '30'); l1.setAttribute('y2', '30');
    const l2 = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    l2.setAttribute('x1', '30'); l2.setAttribute('y1', '10');
    l2.setAttribute('x2', '10'); l2.setAttribute('y2', '30');
    svg.append(l1, l2);
  } else {
    // Circle
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', '20'); circle.setAttribute('cy', '20');
    circle.setAttribute('r', '11');
    svg.appendChild(circle);
  }

  return svg;
}

/* ────────────────────────────────────────────────────────────
   6. BOARD RENDERING
   ──────────────────────────────────────────────────────────── */

/** Fully rebuild the 9-cell board in the DOM. */
function renderBoard() {
  dom.board.innerHTML = '';

  state.board.forEach((val, i) => {
    const cell = document.createElement('div');
    cell.className = 'cell' + (val ? ` ${val} taken` : '');
    cell.setAttribute('role', 'gridcell');
    cell.setAttribute('aria-label', val ? `Cell ${i + 1}: ${val}` : `Cell ${i + 1}: empty`);
    cell.dataset.index = i;

    if (val) {
      cell.appendChild(createMark(val));
    }

    cell.addEventListener('click', handleCellClick);
    dom.board.appendChild(cell);
  });

  // Lock board if AI is thinking or game is over
  dom.board.classList.toggle('board-locked', state.gameOver || state.isAiTurn);
}

/** Highlight winning cells with the win-cell class. */
function highlightWinCells(player) {
  const combo = getWinningCombo(state.board, player);
  if (!combo) return;

  const cells = dom.board.querySelectorAll('.cell');
  combo.forEach(i => cells[i].classList.add('win-cell'));
  drawWinLine(combo, player);
}

/** Animate the win line SVG across the winning combination. */
function drawWinLine(combo, player) {
  const comboIndex = WIN_COMBOS.findIndex(c => c.join() === combo.join());
  if (comboIndex < 0) return;

  const [x1f, y1f, x2f, y2f] = WIN_LINE_COORDS[comboIndex];
  const size = 300; // matches SVG viewBox

  dom.winLine.setAttribute('x1', x1f * size);
  dom.winLine.setAttribute('y1', y1f * size);
  dom.winLine.setAttribute('x2', x2f * size);
  dom.winLine.setAttribute('y2', y2f * size);

  const colour = player === 'X'
    ? 'rgba(232,84,122,0.75)'
    : 'rgba(91,156,246,0.75)';
  dom.winLine.setAttribute('stroke', colour);
  dom.winLine.style.color = colour;

  // Force reflow then trigger the CSS dash animation
  dom.winLine.classList.remove('animate');
  void dom.winLine.offsetWidth;
  dom.winLine.classList.add('animate');
}

/** Hide the win line. */
function clearWinLine() {
  dom.winLine.classList.remove('animate');
  dom.winLine.setAttribute('stroke', 'transparent');
}

/* ────────────────────────────────────────────────────────────
   7. STATUS PANEL
   ──────────────────────────────────────────────────────────── */

/**
 * Update the status panel content and visual state.
 * @param {'human'|'ai'|'win-human'|'win-ai'|'draw'} stateKey
 */
function setStatus(stateKey) {
  const panel = dom.statusPanel;

  // Remove all state classes
  panel.classList.remove('state-human', 'state-ai', 'state-win', 'state-draw');

  switch (stateKey) {
    case 'human':
      panel.classList.add('state-human');
      dom.statusMain.textContent  = 'Your turn';
      dom.statusHint.textContent  = 'Click any empty cell to play';
      break;

    case 'ai':
      panel.classList.add('state-ai');
      dom.statusMain.innerHTML =
        'AI is thinking' +
        '<span class="thinking-dots" aria-hidden="true">' +
          '<span class="thinking-dot"></span>' +
          '<span class="thinking-dot"></span>' +
          '<span class="thinking-dot"></span>' +
        '</span>';
      dom.statusHint.textContent = 'Minimax evaluating game tree…';
      break;

    case 'win-human':
      panel.classList.add('state-win');
      dom.statusMain.textContent = '🎉 You win!';
      dom.statusHint.textContent = 'Impressive — you beat the algorithm';
      break;

    case 'win-ai':
      panel.classList.add('state-ai');
      dom.statusMain.textContent = 'AI wins';
      dom.statusHint.textContent = 'Minimax played perfectly — try again';
      break;

    case 'draw':
      panel.classList.add('state-draw');
      dom.statusMain.textContent = 'Draw!';
      dom.statusHint.textContent = 'Both sides played optimally';
      break;
  }
}

/* ────────────────────────────────────────────────────────────
   8. SCOREBOARD
   ──────────────────────────────────────────────────────────── */

/** Refresh the score numbers and animate the changed value. */
function updateScore(winner) {
  let el = null;

  if (winner === 'human') {
    state.score.human++;
    el = dom.scoreHuman;
    dom.barHuman.classList.add('active');
    dom.barAI.classList.remove('active');
    dom.barDraw.classList.remove('active');
  } else if (winner === 'ai') {
    state.score.ai++;
    el = dom.scoreAI;
    dom.barAI.classList.add('active');
    dom.barHuman.classList.remove('active');
    dom.barDraw.classList.remove('active');
  } else {
    state.score.draw++;
    el = dom.scoreDraw;
    dom.barDraw.classList.add('active');
    dom.barHuman.classList.remove('active');
    dom.barAI.classList.remove('active');
  }

  dom.scoreHuman.textContent = state.score.human;
  dom.scoreAI.textContent    = state.score.ai;
  dom.scoreDraw.textContent  = state.score.draw;

  // Bump animation on the changed score
  if (el) {
    el.classList.remove('bump');
    void el.offsetWidth; // reflow
    el.classList.add('bump');
  }
}

/* ────────────────────────────────────────────────────────────
   9. GAME FLOW
   ──────────────────────────────────────────────────────────── */

/** Handle a click on a board cell. */
function handleCellClick(e) {
  const idx = parseInt(e.currentTarget.dataset.index, 10);

  if (state.gameOver || state.isAiTurn) return;
  if (state.board[idx]) return;

  placeMark(idx, state.humanSym);

  if (checkTerminal(state.humanSym, 'human')) return;

  // Hand off to AI
  state.isAiTurn = true;
  dom.board.classList.add('board-locked');
  setStatus('ai');

  state.thinkTimer = setTimeout(doAiMove, AI_DELAY);
}

/** Execute the AI's move. */
function doAiMove() {
  const move = getBestMove(
    [...state.board],
    state.aiSym,
    state.humanSym,
    dom.difficultyEl.value
  );

  if (move < 0) return;

  placeMark(move, state.aiSym);

  if (checkTerminal(state.aiSym, 'ai')) return;

  // Back to human
  state.isAiTurn = false;
  dom.board.classList.remove('board-locked');
  setStatus('human');
}

/**
 * Place a mark on the logical board and re-render.
 * @param {number} idx    Cell index 0–8
 * @param {string} symbol 'X' or 'O'
 */
function placeMark(idx, symbol) {
  state.board[idx] = symbol;
  renderBoard();
}

/**
 * Check if the game is over after a move.
 * @param {string} symbol   The symbol just played
 * @param {'human'|'ai'} who  Who just moved
 * @returns {boolean} true if game ended
 */
function checkTerminal(symbol, who) {
  if (hasWon(state.board, symbol)) {
    state.gameOver = true;
    dom.board.classList.add('board-locked');
    highlightWinCells(symbol);

    if (who === 'human') {
      setStatus('win-human');
      updateScore('human');
    } else {
      setStatus('win-ai');
      updateScore('ai');
    }
    return true;
  }

  if (emptyCells(state.board).length === 0) {
    state.gameOver = true;
    dom.board.classList.add('board-locked');
    setStatus('draw');
    updateScore('draw');
    return true;
  }

  return false;
}

/* ────────────────────────────────────────────────────────────
   10. GAME INITIALISATION
   ──────────────────────────────────────────────────────────── */

/** Start (or restart) a fresh game. */
function initGame() {
  // Cancel any pending AI move
  if (state.thinkTimer) clearTimeout(state.thinkTimer);

  // Reset logical state
  state.board    = Array(9).fill(null);
  state.gameOver = false;
  state.humanSym = dom.btnX.classList.contains('active') ? 'X' : 'O';
  state.aiSym    = state.humanSym === 'X' ? 'O' : 'X';
  state.isAiTurn = state.humanSym === 'O'; // If human chose O, AI starts

  // Update labels
  dom.humanLabel.textContent = `You · ${state.humanSym}`;
  dom.aiLabel.textContent    = `AI · ${state.aiSym}`;

  // Update difficulty badge
  const diffMap = { easy: 'Easy', medium: 'Medium', hard: 'Hard' };
  dom.modeLabel.textContent = diffMap[dom.difficultyEl.value] ?? 'Hard';

  clearWinLine();
  renderBoard();

  if (state.isAiTurn) {
    // AI opens first
    setStatus('ai');
    state.thinkTimer = setTimeout(doAiMove, AI_DELAY + 200);
  } else {
    setStatus('human');
  }
}

/* ────────────────────────────────────────────────────────────
   11. CONTROLS & EVENT LISTENERS
   ──────────────────────────────────────────────────────────── */

/** Handle symbol toggle (X/O buttons). */
function handleSymbolToggle(e) {
  const btn = e.currentTarget;
  const sym = btn.dataset.symbol;

  dom.btnX.classList.toggle('active', sym === 'X');
  dom.btnO.classList.toggle('active', sym === 'O');
  dom.btnX.setAttribute('aria-pressed', sym === 'X');
  dom.btnO.setAttribute('aria-pressed', sym === 'O');

  initGame();
}

dom.btnX.addEventListener('click', handleSymbolToggle);
dom.btnO.addEventListener('click', handleSymbolToggle);

dom.difficultyEl.addEventListener('change', initGame);

dom.restartBtn.addEventListener('click', initGame);

dom.resetScoreBtn.addEventListener('click', () => {
  state.score = { human: 0, ai: 0, draw: 0 };
  dom.scoreHuman.textContent = 0;
  dom.scoreAI.textContent    = 0;
  dom.scoreDraw.textContent  = 0;
  dom.barHuman.classList.remove('active');
  dom.barAI.classList.remove('active');
  dom.barDraw.classList.remove('active');
  initGame();
});

/* ────────────────────────────────────────────────────────────
   12. BOOT
   ──────────────────────────────────────────────────────────── */

initGame();
