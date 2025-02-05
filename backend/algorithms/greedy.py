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

        # Iterate over all available pieces for the player
        for piece in self.player.get_available_pieces():
            # Iterate over all possible rotations and flips of the piece
            for transformed_piece in self.get_all_transformations(piece):
                # Iterate over all possible positions on the board
                for x in range(self.board.width):
                    for y in range(self.board.height):
                        # Check if the piece can be placed at the current position
                        if self.board.can_place_piece(transformed_piece, x, y, self.player):
                            # Evaluate the move
                            score = self.evaluate_move(transformed_piece, x, y)
                            # Update the best move if the current move has a higher score
                            if score > max_score:
                                max_score = score
                                best_move = {'piece': transformed_piece, 'position': {'x': x, 'y': y}}

        return best_move

    def get_all_transformations(self, piece: Piece):
        transformations = []
        for rotation in range(4):
            rotated_piece = piece.rotate(rotation)
            transformations.append(rotated_piece)
            transformations.append(rotated_piece.flip())
        return transformations

    def evaluate_move(self, piece: Piece, x: int, y: int) -> int:
        # Evaluation criteria
        score = 0

        # 1. Number of squares covered by the piece
        score += piece.shape.sum()

        # 2. Proximity to the center of the board
        center_x, center_y = self.board.grid.shape[0] // 2, self.board.grid.shape[1] // 2
        distance_to_center = abs(center_x - x) + abs(center_y - y)
        score -= distance_to_center  # Prefer moves closer to the center

        # 3. Number of corners touched
        if self.board.validator.touching_corner(piece, x, y, self.player):
            score += 10  # Arbitrary value to prioritize touching corners

        return score

