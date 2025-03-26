import os  # Add import for file operations
from backend.board import Board
from backend.player import Player
from backend.piece import Piece
from backend.move_validator import MoveValidator


class GameManager:
    def __init__(self, player1, player2, player3, player4):
        self.players = [player1, player2, player3, player4]
        self.current_turn = 0
        self.board = Board()
        self.game_over = False
        self.move_log_file = None  # Initialize log file attribute
        self.start_new_game()

    def start_new_game(self):
        """Initialize a new game and create a new log file in the 'game_move_files' directory."""
        directory = os.path.join(os.path.dirname(__file__), "../game_move_files")
        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
        self.move_log_file = os.path.join(directory, f"game_moves_{self.current_turn}.txt")
        with open(self.move_log_file, "w") as file:
            file.write("Move Log for New Game\n")
            file.write("=====================\n")

    def log_move(self, player_id, piece_name, x, y):
        """Log a move to the file."""
        with open(self.move_log_file, "a") as file:
            file.write(f"Player {player_id} placed {piece_name} at ({x}, {y})\n")

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def check_game_over(self):
        # Check if all players have no valid moves left
        for player in self.players:
            valid_moves = player.find_all_valid_moves(self.board)
            if valid_moves:
                return False
        return True

    def play_turn(self):
        current_player = self.players[self.current_turn]
        print(f"Player {current_player.player_id}'s turn")

        valid_moves = current_player.find_all_valid_moves(self.board)
        print(f"Player {current_player.player_id} has {len(valid_moves)} valid moves available.")

        move = None
        attempts = 0
        while move is None and attempts < 3:  # Limit the number of attempts
            move = current_player.choose_move(self.board)
            attempts += 1
        
        if move is None:
            print("No valid move made. Skipping turn.")
            self.next_turn()
            return

        original_piece, piece, x, y = move
        if self.board.place_piece(piece, x, y, current_player):
            current_player.remove_piece(original_piece)
            self.board.display_board()
            # ✅ Log the move
            self.log_move(current_player.player_id, original_piece.name, x, y)
            self.next_turn()
        else:
            print("Invalid move. Try again.")

        if self.check_game_over():
            self.game_over = True
            print("Game over!")
    
    def play_game(self):
        while not self.game_over:
            self.play_turn()