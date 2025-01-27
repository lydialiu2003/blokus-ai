import unittest
from bitboard import Bitboard, piece_dict, Pieces

class TestBitboard(unittest.TestCase):
    def setUp(self):
        self.bitmask = Pieces(piece_dict["L5"])

    def testpieces(self):
        print("Base Shape:")
        print(self.bitmask.base)
        print("\nVariants:")
        print(self.bitmask)


if __name__ == "__main__":
    unittest.main()