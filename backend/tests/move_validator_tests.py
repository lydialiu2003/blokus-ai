import unittest
import numpy as np
from backend.move_validator import MoveValidator

"""
TEST COMMAND
python3 -m unittest backend.tests.move_validator_tests
"""

class MockPiece:
    def __init__(self, shape):
        self.shape = np.array(shape)

class MockPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

class TestMoveValidator(unittest.TestCase):
    def setUp(self):
        self.grid = np.zeros((20, 20), dtype=int)
        self.validator = MoveValidator(self.grid)
        self.player1 = MockPlayer(1)

    def test_within_bounds(self):
        # Test within bounds
        piece = MockPiece([[1, 1], [1, 1]])
        self.assertTrue(self.validator.within_bounds(piece, 0, 0))
        self.assertFalse(self.validator.within_bounds(piece, 19, 19))

    def test_not_overlapping(self):
        # Test not overlapping
        piece = MockPiece([[1, 1], [1, 1]])
        self.grid[0, 0] = 1
        self.assertFalse(self.validator.not_overlapping(piece, 0, 0))
        self.assertTrue(self.validator.not_overlapping(piece, 1, 1))

    def test_touching_corner(self):
        # Test touching corner
        piece = MockPiece([[1, 1], [1, 1]])
        self.grid[1, 1] = 1
        self.assertFalse(self.validator.touching_corner(piece, 0, 0, self.player1))  # Overlapping, should be False
        self.assertFalse(self.validator.touching_corner(piece, 0, 2, self.player1))   # Touching corner, should be True
        self.assertFalse(self.validator.touching_corner(piece, 2, 0, self.player1))   # Touching corner, should be True
        self.assertTrue(self.validator.touching_corner(piece, 2, 2, self.player1))  # Not touching, should be False