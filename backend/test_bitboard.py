import unittest
from bitboard import Bitboard, piece_dict, Pieces, BlokusGame

class TestBitboard(unittest.TestCase):
    def setUp(self):
        self.game = BlokusGame()

    def test_place_piece_player1(self):
        self.game.place_piece(1, "L4", 0, 0)
        self.game.place_piece(1, "L4", 0, 0)
        self.game.place_piece(1, "L4", 0, 0)
        
        # Print the bitboard for player 1 to visually inspect the placement
        print(self.game.players[1])

if __name__ == "__main__":
    unittest.main()