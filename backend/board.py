
import numpy as np

class Board:

    def __init__(self):
        self.grid = np.zeros((20, 20), dtype=int)

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
        return self.within_bounds(piece, x, y) and \
               self.not_overlapping(piece, x, y) and \
               self.touching_corner(piece, x, y, player)
    
    def within_bounds(self, piece, x, y):
        # Check bounds
        piece_height, piece_width = piece.shape.shape
        return 0 <= x < 20 - piece_height + 1 and 0 <= y < 20 - piece_width + 1

    def not_overlapping(self, piece, x, y):
        # Check overlap
        piece_height, piece_width = piece.shape.shape
        for i in range(piece_height):
            for j in range(piece_width):
                if piece.shape[i, j] == 1:  # If part of the piece is present at this cell
                    if self.grid[x + i, y + j] != 0:  # If the cell is not empty
                        return False
        return True
    
    def touching_corner(self, piece, x, y, player):
        # Check if the piece only touches the corners of other pieces
        piece_height, piece_width = piece.shape.shape
        for i in range(piece_height):
            for j in range(piece_width):
                if piece.shape[i, j] == 1:  # If part of the piece is present at this cell
                    # Check surrounding cells to ensure touching only corners
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]  # Adjacent cells
                    for ni, nj in neighbors:
                        if 0 <= ni < 20 and 0 <= nj < 20:  # Ensure within bounds
                            if self.grid[x + ni, y + nj] != 0 and self.grid[x + ni, y + nj] != player.player_id:
                                return False
        return True