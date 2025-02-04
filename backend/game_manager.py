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
    
    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def check_game_over(self):
        # Check if all players have no pieces left or cannot make a valid move
        for player in self.players:
            if any(self.board.is_valid(piece, x, y, player) for piece in player.pieces for x in range(20) for y in range(20)):
                return False
        return True

    def play_turn(self):
        current_player = self.players[self.current_turn]
        print(f"Player {current_player.player_id}'s turn")

        move = None
        attempts = 0
        while move is None and attempts < 3:  # Limit the number of attempts
            move = current_player.choose_move(self.board)
            attempts += 1
        
        if move is None:
            print("No valid move made. Skipping turn.")
            self.next_turn()
            return

        piece, x, y = move
        if self.board.place_piece(piece, x, y, current_player):
            current_player.remove_piece(piece)
            self.board.display_board()
            self.next_turn()
        else:
            print("Invalid move. Try again.")

        if self.check_game_over():
            self.game_over = True
            print("Game over!")

    def check_end_game(self):
        for player in self.players:
            move = player.choose_move(self.board)
            if move is not None:
                return False
        
        self.game_over = True
        print("The game is over!")
        return True
    
    def play_game(self):
        while not self.game_over:
            self.play_turn()
    
    # def check_winner(self):
    #     if not self.game_over:
    #         print("The game is not over yet!")
    #         return None
        
    #     # Initialize player scores (for players 1, 2, 3, ...)
    #     player_scores = {player.player_id: 0 for player in self.players}

    #     # Iterate through the entire board and count tiles for each player
    #     for row in self.board.grid:
    #         for cell in row:
    #             if cell != 0:  # Only count if the tile is occupied by a player
    #                 player_scores[cell] += 1
        
    #     # Determine the player with the highest score
    #     winner_id = max(player_scores, key=player_scores.get)
    #     winner = next(player for player in self.players if player.player_id == winner_id)
        
    #     # Announce the winner
    #     print(f"Player {winner.player_id} is the winner with {player_scores[winner_id]} tiles on the board!")
    #     return winner