import pandas as pd
import numpy as np
from py.pieces import Pawn, Rook, Bishop, Queen, King, Knight


class Board():
    # initial state is just for development ease
    # it is a string that is the path to the csv
    cmap = None

    def __init__(self, initalstate=None):
        if initalstate is None:
            self.hmap = np.array(pd.read_csv(
                "src/csv/default.csv", header=None))
        else:
            self.hmap = np.array(pd.read_csv(initalstate, header=None))
        self.cmap = np.copy(self.hmap)
        self.C()

    # converts it to a computer style data
    def C(self):
        self.cmap[self.cmap == "."] = None
        self.cmap[self.cmap == "R"] = Rook(True)
        self.cmap[self.cmap == "r"] = Rook(False)
        self.cmap[self.cmap == "B"] = Bishop(True)
        self.cmap[self.cmap == "b"] = Bishop(False)
        self.cmap[self.cmap == "P"] = Pawn(True)
        self.cmap[self.cmap == "p"] = Pawn(False)
        self.cmap[self.cmap == "Q"] = Queen(True)
        self.cmap[self.cmap == "q"] = Queen(False)
        self.cmap[self.cmap == "K"] = King(True)
        self.cmap[self.cmap == "k"] = King(False)
        self.cmap[self.cmap == "N"] = Knight(True)
        self.cmap[self.cmap == "n"] = Knight(False)

    # f= from
    # t= to
    # both should be tuples representing (x, y)
    def move(self, f, t):
        self.hmap[t[::-1]], self.hmap[f[::-1]] = self.hmap[f[::-1]], "."
        self.cmap = np.copy(self.hmap)
        self.C()

    # tuple (x, y)
    def isinbounds(self, pos):
        return (
            0 <= pos[0] and
            pos[0] < 8 and
            0 <= pos[1] and
            pos[1] < 8
        )

    # tuple (x, y)
    def isoccupied(self, pos):
        if self.isinbounds(pos):
            if self.cmap[pos[::-1]] is None:
                return False
            else:
                return True
        else:
            return True

    # tuple (x, y)
    def iscapturable(self, pos, team):
        if self.isoccupied(pos) and self.isinbounds(pos):
            return self.cmap[pos[::-1]].team != team
        else:
            return False

    # tuple (x, y)
    def listMoves(self, pos):
        return self.cmap[pos[::-1]].listMoves(pos, self)


class Game():
    lastClickedPiece = None
    lastMovesList = [None, None]

    def __init__(self, initalstate=None):
        self.board = Board(initalstate)

    def move(self, f, t):
        self.board.move(f, t)
