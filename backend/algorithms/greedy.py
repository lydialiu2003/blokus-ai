from backend.board import Board
from backend.piece import Piece
from backend.player import Player
import numpy as np

def debug_print(message, piece=None, x=None, y=None, validation=None):
    print("\nDEBUG:", message)
    if piece is not None:
        print(f"Piece: {piece.name}")
        print("Shape:\n", piece.shape)
    if x is not None and y is not None:
        print(f"Position: ({x}, {y})")
    if validation is not None:
        print(f"Validation result: {validation}")
    print("-" * 50)

class GreedyAI(Player):
    def __init__(self, player_id, pieces):
        super().__init__(player_id, pieces)
        self.board_center = 10  # For a 20x20 board

    def find_all_valid_first_moves(self, board):
        """Find all valid first moves (must touch a corner)"""
        valid_first_moves = []
        corners = [(0, 0), (0, board.size-1), (board.size-1, 0), (board.size-1, board.size-1)]
        
        for piece in self.pieces:
            for orientation in piece.all_orientations():
                oriented_piece = Piece(orientation, piece.name)
                height, width = oriented_piece.shape.shape
                
                # Try placing directly at corners
                for x, y in corners:
                    if board.is_valid(oriented_piece, x, y, self):
                        debug_print(f"Found valid first move at corner", oriented_piece, x, y)
                        valid_first_moves.append((piece, oriented_piece, x, y))
        
        debug_print(f"Found {len(valid_first_moves)} valid first moves")
        return valid_first_moves

    def calculate_utility(self, piece, x, y, board):
        """Calculate utility score for a move based on:
        1. Number of tiles in piece
        2. Distance to center
        3. Number of players blocked"""
        
        # Create a board copy for evaluation
        test_board = Board(board.size)
        test_board.grid = np.copy(board.grid)
        
        if not test_board.is_valid(piece, x, y, self):
            return float('-inf')
            
        # Base score from number of tiles
        tile_count = int(np.sum(piece.shape))
        
        # If board is full, return -inf
        if np.all(board.grid != 0):
            return float('-inf')
            
        # If it's first move, prioritize larger pieces
        if np.all(board.grid == 0):
            return float(1000 + tile_count)  # Let find_all_valid_moves handle corner validation
        
        # Calculate distance from closest tile to center
        min_distance = float('inf')
        height, width = piece.shape.shape
        for i in range(height):
            for j in range(width):
                if piece.shape[i][j] == 1:
                    tile_x, tile_y = x + i, y + j
                    distance = (abs(tile_x - self.board_center) + 
                              abs(tile_y - self.board_center)) / 2
                    min_distance = min(min_distance, distance)
        
        # Calculate blocking score
        board_copy = Board(board.size)
        board_copy.grid = np.copy(board.grid)
        board_copy.place_piece(piece, x, y, self)
        
        blocked_score = 0
        for player_id in range(1, 5):
            if player_id != self.player_id:
                test_player = Player(player_id, self.pieces)
                moves_before = len(test_player.find_all_valid_moves(board))
                moves_after = len(test_player.find_all_valid_moves(board_copy))
                if moves_after < moves_before:
                    blocked_score += 1
        
        return float(tile_count + min_distance + blocked_score)

    def choose_move(self, board):
        debug_print("Starting choose_move")
        
        # Early return if board is full
        if np.all(board.grid != 0):
            debug_print("Board is full - no valid moves possible")
            return None
            
        # Use different move finding strategy for first move
        if np.all(board.grid == 0):
            debug_print("First move detected - finding corner moves")
            valid_moves = self.find_all_valid_first_moves(board)
            if valid_moves:
                # For first move, just take the first valid corner move
                return valid_moves[0]
        else:
            valid_moves = self.find_all_valid_moves(board)
            
        debug_print(f"Found {len(valid_moves)} potential moves")
        
        if not valid_moves:
            debug_print("No valid moves found")
            return None
            
        # Find best move
        best_score = float('-inf')
        best_move = None
        
        for original_piece, oriented_piece, x, y in valid_moves:
            utility = self.calculate_utility(oriented_piece, x, y, board)
            debug_print(f"Evaluating move", oriented_piece, x, y, f"Score: {utility}")
            if utility > best_score:
                best_score = utility
                best_move = (original_piece, oriented_piece, x, y)
                debug_print("New best move found")
        
        if best_move:
            return best_move
            
        return None