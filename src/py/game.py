import pandas as pd
import numpy as np
from py.pieces import King, Queen, Rook, Knight, Bishop, Pawn


class Board():
    # initial state is just for development ease
    # it is a string that is the path to the csv
    cmap = None

    def __init__(self, hmap):
        self.hmap = hmap
        self.cmap = np.copy(self.hmap)
        self.C()

    # converts it to a computer style data
    def C(self):
        self.cmap[self.cmap == "."] = None
        self.cmap[self.cmap == "K"] = King(True)
        self.cmap[self.cmap == "k"] = King(False)
        self.cmap[self.cmap == "Q"] = Queen(True)
        self.cmap[self.cmap == "q"] = Queen(False)
        self.cmap[self.cmap == "R"] = Rook(True)
        self.cmap[self.cmap == "r"] = Rook(False)
        self.cmap[self.cmap == "N"] = Knight(True)
        self.cmap[self.cmap == "n"] = Knight(False)
        self.cmap[self.cmap == "B"] = Bishop(True)
        self.cmap[self.cmap == "b"] = Bishop(False)
        self.cmap[self.cmap == "P"] = Pawn(True)
        self.cmap[self.cmap == "p"] = Pawn(False)

    # f= from
    # t= to
    # both should be tuples representing (x, y)
    def move(self, f, t):
        self.hmap[t[::-1]], self.hmap[f[::-1]] = self.hmap[f[::-1]], "."
        self.cmap[t[::-1]], self.cmap[f[::-1]] = self.cmap[f[::-1]], None

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
                if type(self.cmap[pos[::-1]]) is King:
                    return "K" if self.cmap[pos[::-1]].team else "k"
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
    def isvulnerable(self, pos, team):
        for x in range(8):
            for y in range(8):
                cellpos = (x, y)
                cell = self.cmap[cellpos[::-1]]
                if cell is None:
                    continue
                if cell.team is team:
                    continue
                if type(cell) is King:
                    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0),
                            (1, 1), (-1, -1), (-1, 1), (1, -1)]
                    if pos in [(dir[0] + cellpos[0], dir[1] + cellpos[1]) for dir in dirs]:
                        return True
                    continue
                moves = cell.listMoves(cellpos, self)
                if pos in moves[0]:
                    return True
        return False

    # tuple (x, y)
    def listMoves(self, pos):
        return self.cmap[pos[::-1]].listMoves(pos, self)

    def createEnv(self):
        return Board(np.copy(self.hmap))

    def getKingPos(self, team):
        return tuple(np.asarray(np.where(self.hmap == ("K" if team else "k"))).T.tolist()[0])


class Game():
    lastClickedPiece = None
    lastMovesList = [None, None]
    history = []

    def __init__(self, initalstate=None):
        if initalstate is None:
            hmap = np.array(pd.read_csv(
                "src/csv/default.csv", header=None))
        else:
            hmap = np.array(pd.read_csv(initalstate, header=None))
        self.board = Board(hmap)

    def move(self, f, t):
        self.board.move(f, t)
