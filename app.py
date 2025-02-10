from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from backend.board import Board
from backend.piece import pieces
from backend.player import Player
from backend.move_validator import MoveValidator

app = Flask(__name__)
CORS(app)

# Initialize players and board
players = {i: Player(i, list(pieces.values())) for i in range(1, 5)}
board = Board(size=20)
board.current_player = 1

@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify({'board': board.grid.tolist(), 'current_player': board.current_player})

@app.route('/get_pieces', methods=['GET'])
def get_pieces():
    current_player = board.current_player
    current_player_pieces = players[current_player].pieces
    pieces_data = [{"name": piece.name, "shape": piece.shape.tolist()} for piece in current_player_pieces]
    return jsonify({"pieces": pieces_data})

@app.route('/rotate_piece_hover', methods=['POST'])
def rotate_piece_hover():
    """Rotate a piece on hover and return new shape."""
    data = request.json
    piece_name = data.get("piece")

    for player in players.values():
        for piece in player.pieces:
            if piece.name == piece_name:
                piece.rotate()
                return jsonify({"shape": piece.shape.tolist()})

    return jsonify({"error": "Piece not found"}), 404

@app.route('/rotate_piece_keypress', methods=['POST'])
def rotate_piece_keypress():
    """Rotate or flip a piece when 'r' or 'f' is pressed."""
    data = request.json
    piece_name = data.get("piece")
    action = data.get("action")  # "rotate" or "flip"

    for player in players.values():
        for piece in player.pieces:
            if piece.name == piece_name:
                if action == "rotate":
                    piece.rotate()
                elif action == "flip":
                    piece.flip()
                return jsonify({"shape": piece.shape.tolist()})

    return jsonify({"error": "Piece not found"}), 404

@app.route("/place_piece", methods=["POST"])
def place_piece():
    """Attempt to place a piece on the board."""
    data = request.json
    piece_name = data.get("piece")
    piece_shape_list = data.get("shape")  # ✅ Get shape as list of lists
    x, y = data.get("x"), data.get("y")
    current_player = board.current_player

    # ✅ Ensure `piece_shape_list` is converted to tuple of tuples
    try:
        piece_shape = tuple(tuple(row) for row in piece_shape_list)  # Explicit tuple conversion
        print(f"📌 Converted `piece_shape` to tuple: {piece_shape}")  # Debugging log
        print(f"📌 Type of `piece_shape`: {type(piece_shape)}")  # Should be <class 'tuple'>
    except Exception as e:
        return jsonify({"success": False, "error": f"Invalid shape format: {str(e)}"}), 400

    # ✅ Log the structure before sending it to board
    print(f"📌 Before board.is_valid(): `piece_shape` Type: {type(piece_shape)} - Value: {piece_shape}")

    # ✅ Pass the correctly formatted tuple `piece_shape` to board.is_valid()
    if not board.is_valid(piece_shape, x, y, players[current_player]):
        print("❌ `is_valid()` returned False. Move is not valid.")
        return jsonify({"success": False, "error": "Invalid move."}), 400

    # ✅ Place the piece on the board
    board.place_piece(piece_shape, x, y, players[current_player])
    players[current_player].remove_piece(piece_name)

    # ✅ Rotate turn
    next_player = (current_player % 4) + 1
    board.current_player = next_player  

    return jsonify({
        "success": True,
        "board": board.grid.tolist(),
        "next_player": next_player
    })



if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
