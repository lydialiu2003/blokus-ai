class Bitboard:
    def __init__(self):
        self.board = 0
    
    def index(self, x: int, y: int) -> int:
        return (y * 20) + x
    
    def set_bit(self, x: int, y: int):
        self.board |= (1 << self.index(x, y))

    def clear_bit(self, x: int, y:int):
        self.board &= ~(1 <<self.index(x, y))
    
    def get_bit(self, x: int, y: int) -> bool:
        return (self.board >> self.index(x, y)) & 1
    
    def __str__(self):
        rows = []
        for y in range(20):
            row = ''.join('#' if self.get_bit(x, y) else "." for x in range(20))
            rows.append(row)
        return '\n'.join(rows)
    

piece_dict = {
    "I1" : 0b1000000000000000000000000,
    "I2" : 0b1000010000000000000000000,
    "I3" : 0b1000010000100000000000000,
    "V3" : 0b1000011000000000000000000,
    "I4" : 0b1000010000100001000000000,
    "Z4" : 0b1100001100000000000000000,
    "T4" : 0b1110001000000000000000000,
    "L4" : 0b1000010000110000000000000,
    "O4" : 0b1100011000000000000000000,
    "I5" : 0b1000010000100001000010000,
    "F5" : 0b0110011000010000000000000,
    "P5" : 0b1100011000100000000000000,
    "W5" : 0b1000011000011000000000000,
    "T5" : 0b1110001000010000000000000,
    "X5" : 0b0100011100010000000000000,
    "Z5" : 0b1100001000011000000000000,
    "V5" : 0b1000010000111000000000000,
    "U5" : 0b1010011100000000000000000,
    "N5" : 0b1000011000010000100000000,
    "Y5" : 0b0100011000010000100000000,
    "L5" : 0b1000010000100001100000000
}

class Pieces:
    def __init__(self, shape):
        self.base = shape
        self.variants = self.generate_variants()

    def generate_variants(self):
        variants = set()
        current = self.base
        for _ in range(4):
            variants.add(current)
            variants.add(self.flipped(current))
            current = self.rotate(current)
        return list(variants)
    
    def rotate(self, bitmask):
        rotated = 0
        for y in range(5):
            for x in range(5):
                if (bitmask >> (y * 5 + x)) & 1:
                    rotated |= (1 << ((4 - x) * 5 + y))
        return rotated
    
    def flipped(self, bitmask):
        flipped = 0
        for y in range(5):
            for x in range(5):
                if (bitmask >> (y * 5 + x)) & 1:
                    flipped |= (1 << (y * 5 + (4 - x)))
        return flipped
    
    def __str__(self):
        result = []
        for var in self.variants:
            rows = []
            for y in range(5):
                row = ''.join('#' if (var >> (y * 5 + x)) & 1 else '.' for x in range(5))
                rows.append(row)
            result.append("\n".join(rows))
        return "\n\n".join(result)


