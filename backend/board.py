
import numpy as np
from backend.move_validator import MoveValidator

class Board:

    def __init__(self):
        self.grid = np.zeros((20, 20), dtype=int)
        self.validator = MoveValidator(self.grid)

    def display_board(self):
        # Print boad
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def place_piece(self, piece, x, y, player):
        # Check valid placement
        if self.is_valid(piece, x, y, player):
            # Place piece (mark player_id)
            self.grid[x:x + piece.shape.shape[0], y:y + piece.shape.shape[1]] = player.player_id
            return True
        else:
            return False
        
    def is_valid(self, piece, x, y, player):
        # Validate placement coordinates
        return self.validator.within_bounds(piece, x, y) and \
               self.validator.not_overlapping(piece, x, y) and \
               self.validator.touching_corner(piece, x, y, player)