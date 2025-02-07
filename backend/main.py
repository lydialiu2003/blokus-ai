from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from board import Board
from piece import pieces
from extract_images import extract_images
from player import Player
from move_validator import MoveValidator

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# Load resources
image_path = "static/piece_pixel.png"
player_images = extract_images(image_path)

# Initialize players and board
players = {
    1: Player(1, list(pieces.values())),
    2: Player(2, list(pieces.values())),
    3: Player(3, list(pieces.values())),
    4: Player(4, list(pieces.values())),
}
board = Board(players)

@app.route('/get_board', methods=['GET'])
def get_board():
    """Return the current game board and the current player's turn."""
    return jsonify({
        'board': board.to_list(),
        'current_player': board.current_player
    })

@app.route('/get_pieces', methods=['GET'])
def get_pieces():
    """Return the available pieces for the current player."""
    print(f"🔍 [get_pieces] Current Player: {board.current_player}")
    current_player_pieces = players[board.current_player].pieces
    pieces_data = [
        {"name": piece.name, "shape": piece.shape.tolist()}
        for piece in current_player_pieces
    ]
    print(f"🧩 [get_pieces] Pieces for Player {board.current_player}: {pieces_data}")
    return jsonify({"pieces": pieces_data})
    
@app.route('/place_piece', methods=['POST'])
def place_piece():
    data = request.json
    piece_name = data['piece']
    piece_shape = np.array(data['shape'])
    x, y = data['x'], data['y']
    current_player = board.current_player
    is_first_move = players[current_player].has_made_first_move is False

    print(f"📌 [place_piece] --- DEBUG INFO ---")
    print(f"🎯 Current Player: {current_player}")
    print(f"🎯 Received piece: {piece_name}")
    print(f"🟢 Placement Position -> X: {x}, Y: {y}")

    if not board.validator.is_valid(piece_shape, x, y, current_player, is_first_move):
        print("❌ Invalid Move: Did not pass validation.")
        return jsonify({'success': False, 'error': 'Invalid move.'}), 400

    board.place_piece(piece_shape, x, y, current_player)
    players[current_player].remove_piece(piece_name)
    print(f"✅ Piece {piece_name} placed successfully.")

    next_player = board.get_next_player()
    if next_player is None:
        print("❌ Game Over: No valid moves for any player.")
        return jsonify({'success': True, 'board': board.to_list(), 'next_player': None})
    
    print(f"🔄 Switching to Player {next_player}")
    return jsonify({'success': True, 'board': board.to_list(), 'next_player': next_player})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
