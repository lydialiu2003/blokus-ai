import unittest
from backend.board import Board
from backend.piece import pieces
from backend.algorithms.greedy import GreedyAI

class TestGreedyAI(unittest.TestCase):
    def setUp(self):
        self.board = Board(size=20)
        self.pieces = [pieces['I5'], pieces['O4'], pieces['L4']]  # Test with a few pieces
        self.ai = GreedyAI(player_id=1, pieces=self.pieces)
        print("\n=== Starting New Test ===")
        print("Initial board state:")
        self.board.display_board()
        print("\n")

    def test_evaluate_move(self):
        print("\nTesting evaluate_move:")
        piece = pieces['O4']  # 2x2 square piece
        score = self.ai.evaluate_move(piece, 0, 0, self.board)
        print(f"Score for piece {piece.name} at (0,0): {score}")
        print("Board state after evaluation:")
        self.board.display_board()
        self.assertIsInstance(score, (int, float))
        self.assertTrue(score > 0)

    def test_choose_move_first_turn(self):
        print("\nTesting choose_move_first_turn:")
        move = self.ai.choose_move(self.board)
        if move:
            original_piece, oriented_piece, x, y = move
            print(f"Chosen piece: {original_piece.name} at position ({x},{y})")
            self.board.place_piece(oriented_piece, x, y, self.ai)
            print("Board state after move:")
            self.board.display_board()
        self.assertIsNotNone(move)
        original_piece, oriented_piece, x, y = move
        self.assertTrue(self.board.is_valid(oriented_piece, x, y, self.ai))

    def test_no_valid_moves(self):
        print("\nTesting no_valid_moves:")
        # Fill the board to leave no valid moves
        self.board.grid.fill(2)  # Fill with opponent's pieces
        print("Board state (filled with opponent pieces):")
        self.board.display_board()
        move = self.ai.choose_move(self.board)
        self.assertIsNone(move)

    def tearDown(self):
        print("\n=== Test Complete ===\n")

if __name__ == '__main__':
    unittest.main()
