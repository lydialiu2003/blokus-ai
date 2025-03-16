from backend.board import Board
from backend.piece import Piece
from backend.player import Player
import numpy as np
from copy import deepcopy

class MinimaxAI(Player):
    """
    MinimaxAI implements an AI player for Blokus using the Minimax algorithm with alpha-beta pruning.
    It evaluates moves based on territory control, future move potential, and board position.
    """
    def __init__(self, player_id, pieces, max_depth=3):
        super().__init__(player_id, pieces)
        self.max_depth = max_depth  # How many moves ahead to look
        self.board_center = 10      # Center of the 20x20 board

    def find_all_valid_first_moves(self, board):
        """
        Finds all valid first moves which must be in a corner.
        Returns: List of tuples (original_piece, oriented_piece, x, y)
        """
        valid_first_moves = []
        corners = [(0, 0), (0, board.size-1), (board.size-1, 0), (board.size-1, board.size-1)]
        
        for piece in self.pieces:
            for orientation in piece.all_orientations():
                oriented_piece = Piece(orientation, piece.name)
                for x, y in corners:
                    if board.is_valid(oriented_piece, x, y, self):
                        valid_first_moves.append((piece, oriented_piece, x, y))
        return valid_first_moves

    def calculate_utility(self, board, player_id):
        """
        Evaluates board state using three main factors:
        1. Territory control (number of tiles placed)
        2. Move potential (number of possible future moves)
        3. Board position (proximity to center is better)
        
        Returns: Float representing the board state's value
        """
        # Territory control (number of tiles)
        scores = board.get_score()
        my_tiles = scores.get(player_id, 0)
        
        # Calculate potential future moves (mobility)
        test_player = Player(player_id, self.pieces)
        available_moves = len(test_player.find_all_valid_moves(board))
        
        # Evaluate board position (center control)
        territory_score = 0
        for i in range(board.size):
            for j in range(board.size):
                if board.grid[i][j] == player_id:
                    # Pieces closer to center are worth more
                    distance_to_center = abs(i - self.board_center) + abs(j - self.board_center)
                    territory_score += (20 - distance_to_center)

        # Weight and combine the factors
        # Tiles placed: highest weight (10)
        # Available moves: medium weight (5)
        # Territory position: varies by distance to center
        utility = (my_tiles * 10) + (available_moves * 5) + territory_score
        return float(utility)

    def choose_move(self, board):
        """
        Main method to select the best move using minimax algorithm.
        Handles special cases for first move and full board.
        Returns: Tuple (original_piece, oriented_piece, x, y) or None
        """
        # Handle full board case
        if np.all(board.grid != 0):
            return None
            
        # Handle first move case - choose largest piece for corner
        if np.all(board.grid == 0):
            valid_moves = self.find_all_valid_first_moves(board)
            if valid_moves:
                return max(valid_moves, 
                         key=lambda move: len(np.where(move[1].shape == 1)[0]))

        # Use minimax for all other moves
        best_move = self.minimax(board, self.max_depth, float('-inf'), float('inf'), True)[1]
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Implements minimax algorithm with alpha-beta pruning.
        
        Parameters:
        - board: Current game state
        - depth: How many moves ahead to look
        - alpha: Best value for maximizing player
        - beta: Best value for minimizing player
        - maximizing_player: True if current player is maximizing
        
        Returns: Tuple (score, move)
        """
        # Base cases: reach max depth or no valid moves
        if depth == 0 or not self.find_all_valid_moves(board):
            return self.calculate_utility(board, self.player_id), None

        valid_moves = self.find_all_valid_moves(board)
        if not valid_moves:
            return self.calculate_utility(board, self.player_id), None

        best_move = None
        if maximizing_player:
            # Maximizing player tries to get highest score
            max_eval = float('-inf')
            # Limit move exploration to prevent exponential growth
            for original_piece, oriented_piece, x, y in valid_moves[:10]:
                board_copy = deepcopy(board)
                board_copy.place_piece(oriented_piece, x, y, self)
                
                eval_score, _ = self.minimax(board_copy, depth - 1, alpha, beta, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (original_piece, oriented_piece, x, y)
                
                # Alpha-beta pruning
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval, best_move
        else:
            # Minimizing player tries to get lowest score
            min_eval = float('inf')
            for original_piece, oriented_piece, x, y in valid_moves[:10]:
                board_copy = deepcopy(board)
                board_copy.place_piece(oriented_piece, x, y, self)
                
                eval_score, _ = self.minimax(board_copy, depth - 1, alpha, beta, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (original_piece, oriented_piece, x, y)
                
                # Alpha-beta pruning
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval, best_move