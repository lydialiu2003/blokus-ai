import unittest
from bitboard import Bitboard, piece_dict

class TestBitboard(unittest.TestCase):
    def setUp(self):
        self.bitboard = Bitboard()

    def testindex1(self):
        self.assertEqual(self.bitboard.index(0, 0), 0)

    def testindex3(self):
        self.assertEqual(self.bitboard.index(0, 1), 20)
    
    def testindex2(self):
        self.assertEqual(self.bitboard.index(1, 0), 1)

if __name__ == "__main__":
    unittest.main()