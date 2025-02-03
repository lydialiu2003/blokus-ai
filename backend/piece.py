import numpy as np

class Piece:

    def __init__(self, shape):
        self.shape = np.array(shape)

    def rotate(self):
        self.shape = np.rot90(self.shape)

    def flip(self):
        self.shape = np.fliplr(self.shape)

    def __repr__(self):
        return str(self.shape)

# Define all 21 Blokus pieces
pieces = [
    Piece([[1]], "Single"),
    Piece([[1, 1]], "Double"),
    Piece([[1, 1, 1]], "Triple"),
    Piece([[1, 1, 1, 1]], "Quadruple"),
    Piece([[1, 1, 1, 1, 1]], "Quintuple"),
    Piece([[1, 1], [1, 1]], "Square"),
    Piece([[1, 1, 1], [0, 1, 0]], "T-Shape"),
    Piece([[1, 1, 1], [1, 0, 0]], "L-Shape"),
    Piece([[1, 1, 1], [0, 0, 1]], "Reverse L-Shape"),
    Piece([[1, 1, 1], [0, 1, 1]], "Zigzag"),
    Piece([[0, 1, 1], [1, 1, 0]], "Reverse Zigzag"),
    Piece([[1, 1, 1, 1], [0, 1, 0, 0]], "Extended L"),
    Piece([[1, 1, 1], [0, 1, 0], [0, 1, 0]], "T-Tall"),
    Piece([[1, 1, 1], [1, 0, 1]], "Cross"),
    Piece([[1, 0, 1], [1, 1, 1]], "U-Shape"),
    Piece([[1, 1, 0], [0, 1, 1], [0, 1, 0]], "Diagonal T"),
    Piece([[1, 1, 1, 0], [0, 0, 1, 1]], "Hook"),
    Piece([[1, 1, 1], [0, 1, 1], [0, 0, 1]], "Snake"),
    Piece([[1, 1, 1], [1, 1, 0]], "Big Z"),
    Piece([[1, 1, 0], [0, 1, 0], [0, 1, 1]], "Screw"),
    Piece([[1, 1], [1, 1], [0, 1]], "Pyramid")
]