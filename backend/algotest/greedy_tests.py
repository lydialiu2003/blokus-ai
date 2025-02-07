import unittest
from backend.board import Board
from backend.piece import Piece
from backend.player import Player
from backend.algorithms.greedy import GreedyAI

class TestGreedyAI(unittest.TestCase):
    def setUp(self):
        self.board = Board(width=20, height=20)
        self.player = Player(id=1)
        self.greedy_ai = GreedyAI(board=self.board, player=self.player)

    def test_get_best_move(self):
        # Mock available pieces and board state
        piece = Piece(shape=[[1, 1], [1, 1]])
        self.player.get_available_pieces = lambda: [piece]
        self.board.can_place_piece = lambda p, x, y, player: True
        self.greedy_ai.evaluate_move = lambda p, x, y: 10  # Mock evaluation

        best_move = self.greedy_ai.get_best_move()
        self.assertIsNotNone(best_move)
        self.assertEqual(best_move['piece'], piece)
        self.assertEqual(best_move['position'], {'x': 0, 'y': 0})

    def test_evaluate_move(self):
        piece = Piece(shape=[[1, 1], [1, 1]])
        score = self.greedy_ai.evaluate_move(piece, 10, 10)
        self.assertIsInstance(score, int)

if __name__ == '__main__':
    unittest.main()
