from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from backend.board import Board
from backend.piece import pieces, Piece
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
    piece_shape_list = data.get("shape")
    x, y = data.get("x"), data.get("y")
    current_player = board.current_player

    piece_shape = np.array(piece_shape_list)

    selected_piece = next((p for p in players[current_player].pieces if p.name == piece_name), None)

    if selected_piece is None:
        print(f"❌ DEBUG: Piece {piece_name} not found in Player {current_player}'s inventory!")
        return jsonify({"success": False, "error": "Piece not found"}), 400

    if not board.place_piece(selected_piece, x, y, players[current_player]):
        return jsonify({"success": False, "error": "Invalid move."}), 400

    # call `remove_piece()`
    players[current_player].remove_piece(selected_piece)  

    next_player = (current_player % 4) + 1
    board.current_player = next_player  

    return jsonify({
        "success": True,
        "board": board.grid.tolist(),
        "next_player": next_player,
        "pieces": [{"name": piece.name, "shape": piece.shape.tolist()} for piece in players[next_player].pieces]
    })

@app.route('/end_turn', methods=['POST'])
def end_turn():
    current_player = board.current_player
    next_player = (current_player % 4) + 1

    # Check if the next player has valid moves
    while not players[next_player].find_all_valid_moves(board):
        next_player = (next_player % 4) + 1
        if next_player == current_player:
            break  # All players have no valid moves

    board.current_player = next_player
    return jsonify({
        "success": True,
        "next_player": next_player,
        "board": board.grid.tolist(),
        "pieces": [{"name": piece.name, "shape": piece.shape.tolist()} for piece in players[next_player].pieces]
    })

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
