from backend.board import Board
from backend.piece import Piece
from backend.player import Player

class GreedyAI:
    def __init__(self, board: Board, player: Player):
        self.board = board
        self.player = player

    def get_best_move(self):
        best_move = None
        max_score = -float('inf')

        for piece in self.player.get_available_pieces():
            for x in range(self.board.width):
                for y in range(self.board.height):
                    if self.board.can_place_piece(piece, x, y, self.player):
                        score = self.evaluate_move(piece, x, y)
                        if score > max_score:
                            max_score = score
                            best_move = {'piece': piece, 'position': {'x': x, 'y': y}}

        return best_move

    def evaluate_move(self, piece: Piece, x: int, y: int) -> int:
        # Simple evaluation function: prioritize moves that cover the most squares
        return piece.get_covered_squares()