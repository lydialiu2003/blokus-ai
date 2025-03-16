from backend.board import Board
from backend.piece import Piece
from backend.player import Player
import numpy as np
from copy import deepcopy
import random
import math
import time

class Node:
    def __init__(self, board, player, move=None, parent=None):
        self.board = board
        self.player = player
        self.move = move  # (original_piece, oriented_piece, x, y)
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.untried_moves = player.find_all_valid_moves(board)
        random.shuffle(self.untried_moves)  # Randomize move exploration

    def add_child(self, move, board, player):
        child = Node(board, player, move, self)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.value += result

    def fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=1.414):
        choices = [(child.value / child.visits) + c_param * 
                  math.sqrt(2 * math.log(self.visits) / child.visits)
                  for child in self.children]
        return self.children[choices.index(max(choices))]

class MonteCarloAI(Player):
    def __init__(self, player_id, pieces, simulation_time=1):
        super().__init__(player_id, pieces)
        self.simulation_time = simulation_time
        self.board_center = 10

    def calculate_utility(self, board, player_id):
        """Using the same utility calculation as Minimax/Greedy"""
        # Territory control
        scores = board.get_score()
        my_tiles = scores.get(player_id, 0)
        
        # Move potential
        test_player = Player(player_id, self.pieces)
        available_moves = len(test_player.find_all_valid_moves(board))
        
        # Board position evaluation
        territory_score = 0
        for i in range(board.size):
            for j in range(board.size):
                if board.grid[i][j] == player_id:
                    distance_to_center = abs(i - self.board_center) + abs(j - self.board_center)
                    territory_score += (20 - distance_to_center)

        return float((my_tiles * 10) + (available_moves * 5) + territory_score)

    def choose_move(self, board):
        if np.all(board.grid != 0):
            return None
            
        if np.all(board.grid == 0):
            valid_moves = self.find_all_valid_first_moves(board)
            if valid_moves:
                return max(valid_moves, 
                         key=lambda move: len(np.where(move[1].shape == 1)[0]))

        return self.monte_carlo_search(board)

    def monte_carlo_search(self, board):
        root = Node(board, self)
        end_time = time.time() + self.simulation_time

        while time.time() < end_time:
            node = root
            board_state = deepcopy(board)

            # Selection
            while node.fully_expanded() and node.children:
                node = node.best_child()
                if node.move:
                    board_state.place_piece(node.move[1], node.move[2], node.move[3], node.player)

            # Expansion
            if node.untried_moves:
                move = node.untried_moves[0]
                board_state.place_piece(move[1], move[2], move[3], node.player)
                node = node.add_child(move, board_state, self)

            # Simulation
            result = self.simulate(board_state)

            # Backpropagation
            while node:
                node.update(result)
                node = node.parent

        # Return the move of the best child
        best_child = root.best_child(c_param=0.0)
        return best_child.move

    def simulate(self, board):
        """Run a random simulation from this board state"""
        simulation_board = deepcopy(board)
        current_player = self
        moves_count = 0
        max_moves = 10  # Limit simulation depth

        while moves_count < max_moves:
            valid_moves = current_player.find_all_valid_moves(simulation_board)
            if not valid_moves:
                break

            # Make a random move
            move = random.choice(valid_moves)
            simulation_board.place_piece(move[1], move[2], move[3], current_player)
            moves_count += 1

        # Use the utility function to evaluate the final state
        return self.calculate_utility(simulation_board, self.player_id)

    def find_all_valid_first_moves(self, board):
        """Same as in Minimax/Greedy"""
        valid_first_moves = []
        corners = [(0, 0), (0, board.size-1), (board.size-1, 0), (board.size-1, board.size-1)]
        
        for piece in self.pieces:
            for orientation in piece.all_orientations():
                oriented_piece = Piece(orientation, piece.name)
                for x, y in corners:
                    if board.is_valid(oriented_piece, x, y, self):
                        valid_first_moves.append((piece, oriented_piece, x, y))
        return valid_first_moves
