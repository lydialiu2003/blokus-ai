from backend.board import Board
from backend.piece import Piece
from backend.player import Player
from backend.move_validator import MoveValidator
import numpy as np

class GreedyAI(Player):
    def __init__(self, player_id, pieces):
        super().__init__(player_id, pieces)
        self.board_center = 10  # For a 20x20 board

    def calculate_center_distance(self, x, y, piece):
        """Calculate how close the piece is to the center of the board"""
        height, width = piece.shape.shape
        piece_center_x = x + height/2
        piece_center_y = y + width/2
        distance = ((piece_center_x - self.board_center)**2 + 
                   (piece_center_y - self.board_center)**2)**0.5
        # Normalize distance score (inverse, so closer to center = higher score)
        max_distance = (self.board_center * 2**0.5)  # diagonal distance
        return 1 - (distance / max_distance)

    def count_blocked_moves(self, piece, x, y, board):
        """Count how many potential moves this placement blocks for other players"""
        blocked_positions = 0
        height, width = piece.shape.shape
        
        # Check surrounding positions for potential blocking
        for i in range(-1, height + 1):
            for j in range(-1, width + 1):
                check_x, check_y = x + i, y + j
                if (0 <= check_x < board.size and 
                    0 <= check_y < board.size):
                    # Check if this position could be used by other players
                    # and would be blocked by our piece
                    if board.grid[check_x, check_y] == 0:
                        # If adjacent to our piece, it's blocked
                        if (0 <= i < height and 0 <= j < width and 
                            piece.shape[i][j] == 1):
                            blocked_positions += 1

        return blocked_positions

    def evaluate_move(self, piece, x, y, board):
        # Check if this is a first move (board is empty)
        is_first_move = np.all(board.grid == 0)
        validator = MoveValidator(board.grid)
        
        if is_first_move:
            if validator.first_move(piece, x, y):
                piece_size = int(np.sum(piece.shape))
                return int(1000 + piece_size * 10)
            return float('-inf')
        
        # Regular move evaluation (convert to native Python types)
        piece_size = int(np.sum(piece.shape))
        size_score = piece_size * 10
        center_score = float(self.calculate_center_distance(x, y, piece) * 5)
        blocking_score = self.count_blocked_moves(piece, x, y, board) * 2
        
        return float(size_score + center_score + blocking_score)

    def find_best_move(self, valid_moves, board):
        """Helper method to find the best scored move from valid moves"""
        best_score = float('-inf')
        best_move = None
        validator = MoveValidator(board.grid)
        
        for original_piece, oriented_piece, x, y in valid_moves:
            current_score = self.evaluate_move(oriented_piece, x, y, board)
            print(f"Evaluating {original_piece.name} at ({x},{y}): score = {current_score}")
            
            if current_score > best_score:
                print(f"New best score! Previous: {best_score}, New: {current_score}")
                best_score = current_score
                best_move = (original_piece, oriented_piece, x, y)

        if best_move:
            print(f"Selected move: {best_move[0].name} at ({best_move[2]},{best_move[3]})")
        return best_move

    def choose_move(self, board):
        valid_moves = self.find_all_valid_moves(board)
            
        if not valid_moves:
            print("No valid moves found")
            return None

        best_move = self.find_best_move(valid_moves, board)
        
        if best_move:
            _, oriented_piece, x, y = best_move
            # Final validation using validator
            validator = MoveValidator(board.grid)
            is_first_move = np.all(board.grid == 0)
            
            if is_first_move:
                if not (validator.within_bounds(oriented_piece, x, y) and
                    validator.not_overlapping(oriented_piece, x, y) and
                    validator.first_move(oriented_piece, x, y)):
                    print("Final move validation failed - invalid first move")
                    return None
            else:
                if not (validator.within_bounds(oriented_piece, x, y) and
                    validator.not_overlapping(oriented_piece, x, y) and
                    validator.touching_corner(oriented_piece, x, y, self)):
                    print("Final move validation failed - invalid regular move")
                    return None
                
        return best_move


