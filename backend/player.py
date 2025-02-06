from piece import Piece

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
        
        piece = self.pieces[piece_index]

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
            return piece, x, y
        else:
            print("Invalid move. Try again.")
            return None
            """