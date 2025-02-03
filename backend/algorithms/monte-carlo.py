import random
import math
from backend.board import Board
from backend.piece import Piece
from backend.player import Player

class Node:
    def __init__(self, board: Board, player: Player, parent=None):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.player.get_available_pieces())

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

class MonteCarloTreeSearch:
    def __init__(self, board: Board, player: Player, iterations: int):
        self.board = board
        self.player = player
        self.iterations = iterations

    def get_best_move(self):
        root = Node(self.board, self.player)

        for _ in range(self.iterations):
            node = self.tree_policy(root)
            reward = self.default_policy(node)
            self.backpropagate(node, reward)

        return root.best_child(c_param=0).move

    def tree_policy(self, node):
        while not self.is_terminal(node):
            if not node.is_fully_expanded():
                return self.expand(node)
            else:
                node = node.best_child()
        return node

    def expand(self, node):
        piece = random.choice(self.player.get_available_pieces())
        for x in range(self.board.width):
            for y in range(self.board.height):
                if self.board.can_place_piece(piece, x, y, self.player):
                    new_board = self.board.copy()  # Assuming you have a method to copy the board
                    new_board.place_piece(piece, x, y, self.player)
                    child_node = Node(new_board, self.player, parent=node)
                    node.children.append(child_node)
                    return child_node
        return node

    def default_policy(self, node):
        current_board = node.board.copy()
        current_player = node.player

        while not self.is_terminal(node):
            piece = random.choice(current_player.get_available_pieces())
            x, y = random.randint(0, self.board.width - 1), random.randint(0, self.board.height - 1)
            if current_board.can_place_piece(piece, x, y, current_player):
                current_board.place_piece(piece, x, y, current_player)
                current_player = self.get_next_player(current_player)  # Implement this method

        return self.evaluate_board(current_board)

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.wins += reward
            node = node.parent

    def is_terminal(self, node):
        # Implement your terminal state check here
        return False

    def evaluate_board(self, board):
        # Implement your evaluation function here
        return 0

    def get_next_player(self, current_player):
        # Implement logic to get the next player
        pass