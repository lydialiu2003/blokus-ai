import sys
import os

# Add the parent directory of 'backend' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.board import Board
from backend.player import Player
from backend.piece import pieces
from backend.game_manager import GameManager
from backend.algorithms.greedy import GreedyAI


"""
TEST COMMAND
python3 backend/tests/play_game.py
"""

def main():
    player1 = GreedyAI(1, list(pieces.values()))
    player2 = GreedyAI(2, list(pieces.values()))
    player3 = Player(3, list(pieces.values()))
    player4 = GreedyAI(4, list(pieces.values()))
    game_manager = GameManager(player1, player2, player3, player4)
    game_manager.play_game()

if __name__ == "__main__":
    main()