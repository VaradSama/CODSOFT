"""
Unit tests for Tic-Tac-Toe Minimax AI
Run with: python test_tictactoe.py
"""

import unittest
from tictactoe import (
    create_board, check_winner, is_board_full, get_empty_cells,
    evaluate, minimax, get_ai_move, is_terminal, AI, HUMAN, EMPTY
)

class TestBoardUtils(unittest.TestCase):

    def test_create_board(self):
        board = create_board()
        self.assertEqual(len(board), 9)
        self.assertTrue(all(c == EMPTY for c in board))

    def test_check_winner_row(self):
        board = [AI, AI, AI, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        self.assertTrue(check_winner(board, AI))
        self.assertFalse(check_winner(board, HUMAN))

    def test_check_winner_column(self):
        board = [AI, EMPTY, EMPTY, AI, EMPTY, EMPTY, AI, EMPTY, EMPTY]
        self.assertTrue(check_winner(board, AI))

    def test_check_winner_diagonal(self):
        board = [AI, EMPTY, EMPTY, EMPTY, AI, EMPTY, EMPTY, EMPTY, AI]
        self.assertTrue(check_winner(board, AI))

    def test_no_winner(self):
        board = create_board()
        self.assertFalse(check_winner(board, AI))
        self.assertFalse(check_winner(board, HUMAN))

    def test_board_full(self):
        board = [AI, HUMAN, AI, HUMAN, AI, HUMAN, HUMAN, AI, HUMAN]
        self.assertTrue(is_board_full(board))

    def test_empty_cells(self):
        board = [AI, EMPTY, HUMAN, EMPTY, EMPTY, AI, HUMAN, EMPTY, AI]
        empty = get_empty_cells(board)
        self.assertEqual(sorted(empty), [1, 3, 4, 7])


class TestMinimax(unittest.TestCase):

    def test_ai_blocks_winning_move(self):
        """AI must block human from winning on next move."""
        # Human about to win at position 2
        board = [HUMAN, HUMAN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        move = get_ai_move(board, difficulty="hard")
        self.assertEqual(move, 2)  # AI should block

    def test_ai_takes_winning_move(self):
        """AI must take an immediate win."""
        # AI wins at position 2
        board = [AI, AI, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        move = get_ai_move(board, difficulty="hard")
        self.assertEqual(move, 2)

    def test_evaluate_ai_win(self):
        board = [AI, AI, AI, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        self.assertEqual(evaluate(board), 1)

    def test_evaluate_human_win(self):
        board = [HUMAN, HUMAN, HUMAN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        self.assertEqual(evaluate(board), -1)

    def test_evaluate_draw(self):
        board = create_board()
        self.assertEqual(evaluate(board), 0)

    def test_minimax_prefers_win_over_draw(self):
        """Minimax score for a near-win state should be +1."""
        board = [AI, AI, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        score = minimax(board, 9, True)
        self.assertEqual(score, 1)

    def test_full_game_never_loses(self):
        """AI (hard) should never lose — simulate AI vs AI (both hard) → always draw."""
        board = create_board()
        current_player = AI
        while not is_terminal(board):
            move = get_ai_move(board, "hard")
            board[move] = current_player
            current_player = HUMAN if current_player == AI else AI
        # In a perfect play scenario starting from empty → draw
        self.assertFalse(check_winner(board, HUMAN))


if __name__ == "__main__":
    unittest.main(verbosity=2)
