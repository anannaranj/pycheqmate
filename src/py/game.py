import pandas as pd
import numpy as np
from pieces import Pawn, Rook


class Board():
    # initial state is just for development ease
    # it is a string that is the path to the csv
    cmap = None

    def __init__(self, initalstate=None):
        if initalstate is None:
            self.hmap = np.array(pd.read_csv(
                "../csv/default.csv", header=None))
        else:
            self.hmap = np.array(pd.read_csv(initalstate, header=None))
        self.cmap = np.copy(self.hmap)
        self.C()

    # converts it to a computer style data
    def C(self):
        self.cmap[self.cmap == "."] = None
        self.cmap[self.cmap == "R"] = Rook(True)
        self.cmap[self.cmap == "r"] = Rook(False)
        self.cmap[self.cmap == "P"] = Pawn(True)
        self.cmap[self.cmap == "p"] = Pawn(False)

    # f= from
    # t= to
    # both should be tuples representing (x, y)
    def move(self, f, t):
        self.cmap[t[::-1]], self.cmap[f[::-1]] = self.cmap[f[::-1]], "."
        self.cmap = np.copy(self.hmap)
        self.C()

    def isoccupied(self, pos):
        if (
            0 <= pos[::-1][0] and
            pos[::-1][0] < 8 and
            0 <= pos[::-1][1] and
            pos[::-1][1] < 8
        ):
            if self.cmap[pos[::-1]] is None:
                return False
            else:
                return True
        else:
            return True

    def listMoves(self, pos):
        return self.cmap[pos[::-1]].listMoves(pos, self)


class Game():
    def __init__(self, initalstate):
        self.board = Board(initalstate)


# m = Board("../csv/pawns.csv")
# print(m.listMoves((3, 1)))
# print(m.listMoves((1, 3)))
# print(m.listMoves((3, 5)))
# print(m.listMoves((5, 6)))
m = Board("../csv/rooks.csv")
print(m.listMoves((1, 1)))
