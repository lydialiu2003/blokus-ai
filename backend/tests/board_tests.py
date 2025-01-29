import unittest
import numpy as np
from backend.board import Board

"""
TEST COMMAND
python3 -m unittest backend.tests.board_tests
"""

class MockPiece:
    def __init__(self, shape):
        self.shape = np.array(shape)

class MockPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player1 = MockPlayer(1)
        self.player2 = MockPlayer(2)

    def test_initial_board(self):
        # Test initial board state
        expected_grid = np.zeros((20, 20), dtype=int)
        np.testing.assert_array_equal(self.board.grid, expected_grid)

    def test_within_bounds(self):
        # Test within bounds
        piece = MockPiece([[1, 1], [1, 1]])
        self.assertTrue(self.board.validator.within_bounds(piece, 0, 0))
        self.assertFalse(self.board.validator.within_bounds(piece, 19, 19))

    def test_not_overlapping(self):
        # Test not overlapping
        piece = MockPiece([[1, 1], [1, 1]])
        self.board.grid[0, 0] = 1
        self.assertFalse(self.board.validator.not_overlapping(piece, 0, 0))
        self.assertTrue(self.board.validator.not_overlapping(piece, 1, 1))

    def test_touching_corner(self):
        # Test touching corner
        piece = MockPiece([[1, 1], [1, 1]])
        self.board.grid[1, 1] = 1
        self.assertFalse(self.board.validator.touching_corner(piece, 0, 0, self.player1))
        self.assertTrue(self.board.validator.touching_corner(piece, 2, 2, self.player1))

    def test_is_valid(self):
        # Test is valid
        piece = MockPiece([[1, 1], [1, 1]])
        self.board.grid[2, 2] = 1
        self.assertTrue(self.board.is_valid(piece, 0, 0, self.player1))

    def test_place_piece(self):
        # Test place piece
        piece = MockPiece([[1, 1], [1, 1]])
        self.board.grid[2, 2] = 1
        self.assertTrue(self.board.place_piece(piece, 0, 0, self.player1))

    def test_display_board(self):
        # Test display board
        piece = MockPiece([[1, 1], [1, 1]])
        self.board.grid[2, 2] = 1
        self.board.place_piece(piece, 0, 0, self.player1)
        self.board.display_board()

if __name__ == "__main__":
    unittest.main()