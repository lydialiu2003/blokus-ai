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