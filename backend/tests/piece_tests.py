import unittest
import numpy as np
from backend.piece import Piece

"""
TEST COMMAND
python3 -m unittest backend.tests.piece_tests
"""

class TestPiece(unittest.TestCase):
    def setUp(self):
        # Initialize a piece with a specific shape
        self.piece = Piece([[1, 0], [1, 1]])

    def test_initial_shape(self):
        # Test initial shape
        expected_shape = np.array([[1, 0], [1, 1]])
        np.testing.assert_array_equal(self.piece.shape, expected_shape)

    def test_rotate(self):
        # Test rotate method
        self.piece.rotate()
        expected_shape = np.array([[0, 1], [1, 1]])
        np.testing.assert_array_equal(self.piece.shape, expected_shape)

        # Rotate again to verify multiple rotations
        self.piece.rotate()
        expected_shape = np.array([[1, 1], [0, 1]])
        np.testing.assert_array_equal(self.piece.shape, expected_shape)

    def test_flip(self):
        # Test flip method
        self.piece.flip()
        expected_shape = np.array([[0, 1], [1, 1]])
        np.testing.assert_array_equal(self.piece.shape, expected_shape)

        # Flip again to verify multiple flips
        self.piece.flip()
        expected_shape = np.array([[1, 0], [1, 1]])
        np.testing.assert_array_equal(self.piece.shape, expected_shape)

    def test_repr(self):
        # Test __repr__ method
        expected_repr = '[[1 0]\n [1 1]]'
        self.assertEqual(repr(self.piece), expected_repr)

if __name__ == "__main__":
    unittest.main()