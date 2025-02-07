class MoveValidator:
    def __init__(self, grid):
        self.grid = grid

    def first_move(self, piece, x, y):
        corner_coordinates = {(0, 0), (19, 0), (0, 19), (19, 19)}
        piece_height, piece_width = piece.shape
        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i, j] == 1 and (x + i, y + j) in corner_coordinates:
                    return True
        return False

    def within_bounds(self, piece, x, y):
        piece_height, piece_width = piece.shape
        return (
            0 <= x < self.grid.shape[0] and
            0 <= y < self.grid.shape[1] and
            x + piece_height <= self.grid.shape[0] and
            y + piece_width <= self.grid.shape[1]
        )

    def not_overlapping(self, piece, x, y):
        piece_height, piece_width = piece.shape
        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i, j] == 1 and self.grid[x + i, y + j] != 0:
                    return False
        return True
<<<<<<< HEAD

    def touching_corner(self, piece, x, y, player_id):
        piece_height, piece_width = piece.shape
        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i, j] == 1:
                    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        nx, ny = x + i + dx, y + j + dy
                        if 0 <= nx < self.grid.shape[0] and 0 <= ny < self.grid.shape[1]:
                            if self.grid[nx, ny] == player_id:
                                return True
        return False

    def is_valid(self, piece, x, y, player_id, is_first_move):
        if is_first_move:
            return (
                self.first_move(piece, x, y) and
                self.within_bounds(piece, x, y) and
                self.not_overlapping(piece, x, y)
            )
        else:
            return (
                self.touching_corner(piece, x, y, player_id) and
                self.within_bounds(piece, x, y) and
                self.not_overlapping(piece, x, y)
            )
=======
    
    def first_move(self, piece, x, y):
        # Check if the piece is placed at one of the corner coordinates
        piece_height, piece_width = piece.shape.shape
        for i in range(piece_height):
            for j in range(piece_width):
                if piece.shape[i, j] == 1:
                    if (x + i == 0 and y + j == 0) or \
                       (x + i == 0 and y + j == self.grid.shape[1] - 1) or \
                       (x + i == self.grid.shape[0] - 1 and y + j == 0) or \
                       (x + i == self.grid.shape[0] - 1 and y + j == self.grid.shape[1] - 1):
                        return True
        return False
    
    def touching_corner(self, piece, x, y, player):
        # Check if the piece only touches the corners of other pieces
        piece_height, piece_width = piece.shape.shape
        touching_corner = False
        for i in range(piece_height):
            for j in range(piece_width):
                if piece.shape[i, j] == 1:  # If part of the piece is present at this cell
                    # Check adjacent cells to ensure no edge sharing
                    if (x + i > 0 and self.grid[x + i - 1, y + j] == player.player_id) or \
                       (x + i < self.grid.shape[0] - 1 and self.grid[x + i + 1, y + j] == player.player_id) or \
                       (y + j > 0 and self.grid[x + i, y + j - 1] == player.player_id) or \
                       (y + j < self.grid.shape[1] - 1 and self.grid[x + i, y + j + 1] == player.player_id):
                        return False
                    # Check diagonal cells to ensure corner touching
                if piece.shape[i, j] == 1:
                    if (x + i > 0 and y + j > 0 and self.grid[x + i - 1, y + j - 1] == player.player_id) or \
                       (x + i > 0 and y + j < self.grid.shape[1] - 1 and self.grid[x + i - 1, y + j + 1] == player.player_id) or \
                       (x + i < self.grid.shape[0] - 1 and y + j > 0 and self.grid[x + i + 1, y + j - 1] == player.player_id) or \
                       (x + i < self.grid.shape[0] - 1 and y + j < self.grid.shape[1] - 1 and self.grid[x + i + 1, y + j + 1] == player.player_id):
                                touching_corner = True
        return touching_corner
>>>>>>> 2976d133720d239feac6f03fd024d3f8a85be35e
