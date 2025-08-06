from numpy import array, copy, asarray, where
from pandas import DataFrame
# from pandas import DataFrame, read_csv
from py.pieces import King, Queen, Rook, Bishop, Knight, Pawn, dirsLoop


class Board():
    cmap = None

    def __init__(self, hmap):
        self.hmap = hmap
        self.cmap = copy(self.hmap)
        self.C()

    # converts it to a computer style data
    def CBackend(self, pos):
        x, y = pos
        i = self.cmap[(y, x)]
        if i == ".":
            self.cmap[(y, x)] = None
        if i == "K":
            self.cmap[(y, x)] = King(True)
        if i == "k":
            self.cmap[(y, x)] = King(False)
        if i == "Q":
            self.cmap[(y, x)] = Queen(True)
        if i == "q":
            self.cmap[(y, x)] = Queen(False)
        if i == "R":
            self.cmap[(y, x)] = Rook(True)
        if i == "r":
            self.cmap[(y, x)] = Rook(False)
        if i == "B":
            self.cmap[(y, x)] = Bishop(True)
        if i == "b":
            self.cmap[(y, x)] = Bishop(False)
        if i == "N":
            self.cmap[(y, x)] = Knight(True)
        if i == "n":
            self.cmap[(y, x)] = Knight(False)
        if i == "P":
            self.cmap[(y, x)] = Pawn(True)
        if i == "p":
            self.cmap[(y, x)] = Pawn(False)

    def C(self):
        for y in range(8):
            for x in range(8):
                self.CBackend((x, y))

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
        x = dirsLoop([(0, 1), (1, 0), (0, -1), (-1, 0)], pos, self, team)
        for i in sum(x, []):
            p = self.cmap[i[::-1]]
            if (type(p) is Rook or type(p) is Queen) and p.team is not team:
                return True
        y = dirsLoop([(1, 1), (1, -1), (-1, -1), (-1, 1)], pos, self, team)
        for i in sum(y, []):
            p = self.cmap[i[::-1]]
            if (type(p) is Bishop or type(p) is Queen) and p.team is not team:
                return True
        for dir in [(2, 1), (1, 2), (-1, 2), (-2, 1),
                    (-2, -1), (-1, -2), (1, -2), (2, -1)]:
            p = (dir[0] + pos[0], dir[1] + pos[1])
            if self.isinbounds(p) and self.isoccupied(p):
                piece = self.cmap[p[::-1]]
                if type(piece) is Knight and piece.team is not team:
                    return True
        d = {True: -1, False: 1}[team]
        for x in [1, -1]:
            p = (pos[0] + x, pos[1] + d)
            if self.isinbounds(p) and self.isoccupied(p):
                piece = self.cmap[p[::-1]]
                if type(piece) is Pawn and piece.team is not team:
                    return True
        for dir in [(0, 1), (1, 0), (0, -1), (-1, 0),
                    (1, 1), (-1, -1), (-1, 1), (1, -1)]:
            p = (dir[0] + pos[0], dir[1] + pos[1])
            if self.isinbounds(p) and self.isoccupied(p):
                piece = self.cmap[p[::-1]]
                if type(piece) is King and piece.team is not team:
                    return True
        return False

    # tuple (x, y)
    def listMoves(self, pos):
        return self.cmap[pos[::-1]].listMoves(pos, self)

    def createEnv(self):
        return Board(copy(self.hmap))

    def getKingPos(self, team):
        return tuple(asarray(where(self.hmap == ("K" if team else "k"))).T.tolist()[0])[::-1]


class Game():
    lastClickedPiece = None
    lastMovesList = [None, None, None]
    history = []

    # initial state is just for development ease
    # it is a string that is the path to the csv
    def __init__(self, initalstate=None):
        # if initalstate is None:
        #     hmap = np.array(pd.read_csv(
        #         "./csv/default.csv", header=None))
        # else:
        #     hmap = np.array(pd.read_csv(initalstate, header=None))
        default = [x.split(",") for x in [
            "r,n,b,q,k,b,n,r",
            "p,p,p,p,p,p,p,p",
            ".,.,.,.,.,.,.,.",
            ".,.,.,.,.,.,.,.",
            ".,.,.,.,.,.,.,.",
            ".,.,.,.,.,.,.,.",
            "P,P,P,P,P,P,P,P",
            "R,N,B,Q,K,B,N,R",
        ]]
        # hmap = array(read_csv(initalstate, header=None))
        hmap = array(DataFrame(default))
        self.board = Board(hmap)

    def move(self, f, t):
        if hasattr(self.board.cmap[f[::-1]], 'firstMove'):
            if self.board.cmap[f[::-1]].firstMove is None:
                self.board.cmap[f[::-1]].firstMove = len(self.history)
        promotion = None
        if t[1] == 0 and self.board.hmap[f[::-1]] == "P":
            promotion = "P"
        elif t[1] == 7 and self.board.hmap[f[::-1]] == "p":
            promotion = "p"
        self.board.move(f, t)
        self.history.append([f, t])
        return promotion

    def castle(self, type):
        if type == "O-O":
            self.board.move((4, 7), (6, 7))
            self.board.move((7, 7), (5, 7))
        if type == "o-o":
            self.board.move((4, 0), (6, 0))
            self.board.move((7, 0), (5, 0))
        if type == "O-O-O":
            self.board.move((4, 7), (2, 7))
            self.board.move((0, 7), (3, 7))
        if type == "o-o-o":
            self.board.move((4, 0), (2, 0))
            self.board.move((0, 0), (3, 0))
        self.history.append(type)

    def promote(self, pos, piece):
        self.board.hmap[pos[::-1]] = piece
        self.board.cmap[pos[::-1]] = piece
        self.board.CBackend(pos)
