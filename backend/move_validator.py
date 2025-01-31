import numpy as np

class MoveValidator:
    def __init__(self, grid):
        self.grid = grid

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
        touching_corner = False
        for i in range(piece_height):
            for j in range(piece_width):
                if piece.shape[i, j] == 1:  # If part of the piece is present at this cell
                    # Check adjacent cells to ensure no edge sharing
                    adjacent_cells = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    for ni, nj in adjacent_cells:
                        if 0 <= x + ni < 20 and 0 <= y + nj < 20:
                            if self.grid[x + ni, y + nj] != 0:
                                return False
                    # Check diagonal cells to ensure corner touching
                    diagonal_cells = [(i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)]
                    for ni, nj in diagonal_cells:
                        if 0 <= x + ni < 20 and 0 <= y + nj < 20:
                            if self.grid[x + ni, y + nj] == player.player_id:
                                touching_corner = True
        return touching_corner