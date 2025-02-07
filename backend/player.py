<<<<<<< HEAD
from piece import Piece
=======
from backend.piece import Piece
from copy import deepcopy
>>>>>>> 2976d133720d239feac6f03fd024d3f8a85be35e

class Player:
    def __init__(self, player_id, pieces):
        self.player_id = player_id
        self.pieces = pieces  # List of Piece objects
        self.has_made_first_move = False

    def remove_piece(self, piece_name):
        """
        Remove a piece from the player's available pieces by its name.
        """
        found = False
        for piece in self.pieces:
            if piece.name == piece_name:
                self.pieces.remove(piece)
                found = True
                print(f"[remove_piece] Removed piece: {piece_name} from player {self.player_id}")
                break  # Stop after removing one piece
        
        if not found:
            print(f"[remove_piece] ERROR: Piece {piece_name} not found for player {self.player_id}")

    def get_piece(self, piece_name):
        """
        Retrieve a piece object by its name.
        """
        for piece in self.pieces:
            if piece.name == piece_name:
                return piece
        return None
    
    def get_next_player(self):
        """
        Cycle to the next player with valid moves. If none, the game ends.
        """
        print(f"🔄 [get_next_player] Current Player: {self.current_player}")
        for _ in range(len(self.players)):
            self.current_player = (self.current_player % len(self.players)) + 1
            print(f"🟢 Testing Player {self.current_player} for valid moves...")
            if self.players[self.current_player].has_available_moves(self):
                print(f"✅ Player {self.current_player} has valid moves.")
                return self.current_player
        print("❌ Game Over: No players have valid moves.")
        return None

    
    def has_available_moves(self, board):
        """
        Check if the player has any valid moves left.
        """
        print(f"🔍 Checking available moves for Player {self.player_id}")
        is_first_move = not self.has_made_first_move  # Determine if it's the first move
        for piece in self.pieces:
            for x in range(board.grid.shape[0]):
                for y in range(board.grid.shape[1]):
                    if board.validator.is_valid(piece.shape, x, y, self.player_id, is_first_move):
                        print(f"✅ Valid move found for Player {self.player_id} with piece {piece.name} at ({x}, {y})")
                        return True
        print(f"❌ No valid moves left for Player {self.player_id}")
        return False



"""
class Player:
    def __init__(self, player_id, pieces):
        self.player_id = player_id
        self.pieces = pieces

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)

    def choose_move(self, board):
        print(f"Player {self.player_id}, choose a move.")
        
        for i, piece in enumerate(self.pieces):
            print(f"{i}: \n{piece.shape}\n")

        piece_index = int(input("Select a piece by index: "))
        if piece_index < 0 or piece_index >= len(self.pieces):
            print("Invalid selection")
            return None
        
        original_piece = self.pieces[piece_index]
        piece = deepcopy(original_piece)

        # Ask if the player wants to rotate or flip the piece
        while True:
            transform = input("Enter transformations (r for rotate, f for flip, done to finish): ").strip().lower()
            if transform == 'r':
                piece.rotate()
            elif transform == 'f':
                piece.flip()
            elif transform == 'done':
                break
            else:
                print("Invalid input. Enter 'r' to rotate, 'f' to flip, or 'done' to finish.")

        x = int(input("Enter row coordinate: "))
        y = int(input("Enter column coordinate: "))
    
        if board.is_valid(piece, x, y, self):
            return original_piece, piece, x, y
        else:
            print("Invalid move. Try again.")
            return None
<<<<<<< HEAD
            """
=======
        
    def get_all_orientations(self):
        all_orientations = {}
        for piece in self.pieces:
            all_orientations[piece.name] = piece.all_orientations()
        return all_orientations

    def find_all_valid_moves(self, board):
        valid_moves = []
        for piece in self.pieces:
            for orientation in piece.all_orientations():
                orientation_piece = Piece(orientation, piece.name)  # Create a Piece object for each orientation
                for x in range(board.size):
                    for y in range(board.size):
                        if board.is_valid(orientation_piece, x, y, self):
                            valid_moves.append((piece, orientation_piece, x, y))
        return valid_moves
>>>>>>> 2976d133720d239feac6f03fd024d3f8a85be35e
