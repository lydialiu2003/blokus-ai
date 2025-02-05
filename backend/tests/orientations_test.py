import sys
import os

# Add the parent directory of 'backend' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.piece import pieces
from backend.player import Player

"""
TEST COMMAND
python3 backend/tests/orientations_test.py
"""

def main():
    player = Player(1, list(pieces.values()))
    all_orientations = player.get_all_orientations()
    for piece_name, orientations in all_orientations.items():
        print(f"Piece: {piece_name}")
        for i, orientation in enumerate(orientations):
            print(f"Orientation {i + 1}:\n{orientation}\n")

if __name__ == "__main__":
    main()