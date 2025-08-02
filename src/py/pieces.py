import numpy as np
# the piece class is just the fundamental methods and values for all the 6 pieces


class Piece():
    # the team is a boolean, True for white, False for black
    def __init__(self, team):
        self.team = team


def dirsLoop(dirs, pos, m, s):
    ls = [[] for _ in dirs]
    captures = []
    for dir in dirs:
        x = pos
        p = (x[0]+dir[0], x[1]+dir[1])
        while not (m.isoccupied(p) in ["K" if s.team else "k", True]):
            ls[dirs.index(dir)].append(p)
            x = ls[dirs.index(dir)][-1]
            p = (x[0]+dir[0], x[1]+dir[1])
        if m.iscapturable(p, s.team):
            captures.append(p)
    return [sum(ls, []), captures]


class Rook(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        return dirsLoop(dirs, pos, m, self)


class Bishop(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        return dirsLoop(dirs, pos, m, self)


class Queen(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (1, -1), (-1, -1), (-1, 1)]
        return dirsLoop(dirs, pos, m, self)


class Pawn(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        ls = []
        captures = []

        dir = {True: -1, False: 1}
        d = dir[self.team]

        oneblock = (pos[0], pos[1] + d)
        if not m.isoccupied(oneblock):
            ls.append(oneblock)

        twoblocks = (pos[0], pos[1] + 2 * d)
        if pos[1] == 3.5 - 2.5 * d and not m.isoccupied(oneblock) and not m.isoccupied(twoblocks):
            ls.append(twoblocks)

        for x in [1, -1]:
            p = (pos[0] + x, pos[1] + d)
            if m.iscapturable(p, self.team):
                captures.append(p)

        # TODO: missing en passant implementation
        # TODO: missing promotion implementation

        return [ls, captures]


class Knight(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                (-2, -1), (-1, -2), (1, -2), (2, -1)]
        ls = []
        captures = []
        for dir in dirs:
            p = (dir[0] + pos[0], dir[1] + pos[1])
            if not m.isoccupied(p):
                ls.append(p)
            elif m.iscapturable(p, self.team):
                captures.append(p)

        return [ls, captures]


class King(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (-1, -1), (-1, 1), (1, -1)]
        ls = []
        captures = []
        for dir in dirs:
            p = (dir[0] + pos[0], dir[1] + pos[1])
            if m.isinbounds(p):
                if not m.isvulnerable(p, self.team):
                    if not m.isoccupied(p):
                        ls.append(p)
                    elif m.iscapturable(p, self.team):
                        captures.append(p)

        # TODO: missing castling implementation
        return [ls, captures]
