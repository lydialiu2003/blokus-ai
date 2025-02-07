import numpy as np
from move_validator import MoveValidator


class Board:
    def __init__(self, players):
        self.grid = np.zeros((20, 20), dtype=int)  # 20x20 game board grid
        self.validator = MoveValidator(self.grid)  # Initialize the MoveValidator
        self.current_player = 1  # Start with Player 1
        self.players = players

<<<<<<< HEAD
    def is_first_move(self, player_id):
        """Check if the player has made their first move."""
        return not self.players[player_id].has_made_first_move
=======
    def __init__(self, size=20):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.validator = MoveValidator(self.grid)
>>>>>>> 2976d133720d239feac6f03fd024d3f8a85be35e

    def place_piece(self, piece, x, y, player_id):
        """Attempt to place a piece on the board."""
        if self.is_valid(piece, x, y, player_id):
            piece_height, piece_width = piece.shape
            for i in range(piece_height):
                for j in range(piece_width):
                    if piece[i, j] == 1:
                        self.grid[x + i, y + j] = player_id
            self.players[player_id].has_made_first_move = True
            return True
        return False

    def is_valid(self, piece, x, y, player_id):
        """Check if a piece placement is valid."""
        if self.is_first_move(player_id):
            print(f"[is_valid] Checking first move for player {player_id} at ({x}, {y})")
            return (
                self.validator.within_bounds(piece, x, y) and
                self.validator.not_overlapping(piece, x, y) and
                self.validator.first_move(piece, x, y)
            )
        else:
            print(f"[is_valid] Checking regular move for player {player_id} at ({x}, {y})")
            return (
                self.validator.within_bounds(piece, x, y) and
                self.validator.not_overlapping(piece, x, y) and
                self.validator.touching_corner(piece, x, y, player_id)
            )
    def get_next_player(self):
        """
        Cycle to the next player with valid moves. If none, the game ends.
        """
        print(f"🔄 [get_next_player] Current Player: {self.current_player}")
        for _ in range(len(self.players)):
            self.current_player = (self.current_player % len(self.players)) + 1
            print(f"🟢 Testing Player {self.current_player} for valid moves...")
            if self.players[self.current_player].has_available_moves(self):
                print(f"✅ Player {self.current_player} has valid moves.")
                return self.current_player
        print("❌ Game Over: No players have valid moves.")
        return None

        

    def to_list(self):
        """Convert the grid to a list for JSON serialization."""
        return self.grid.tolist()
