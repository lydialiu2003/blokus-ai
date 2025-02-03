import sys
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from board import Board

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Initialize the game board
board = Board()

@app.route('/get_board', methods=['GET'])
def get_board():
    """Return the current game board."""
    return jsonify({'board': board.to_list(), 'current_player': 'A'})  # Default to Player A

@app.route('/place_piece', methods=['POST'])
def place_piece():
    """Mock piece placement for now."""
    data = request.json
    piece = data['piece']
    x, y = data['x'], data['y']

    # Simulate a successful placement
    print(f"Mock placement: Piece {piece} at ({x}, {y})")
    return jsonify({'success': True, 'board': board.to_list(), 'next_player': 'B'})  # Default Player B

if __name__ == '__main__':
    app.run(debug=True)
