import numpy as np
# the piece class is just the fundamental methods and values for all the 6 pieces


class Piece():
    # the team is a boolean, True for white, False for black
    def __init__(self, team):
        self.team = team


def dirsLoop(dirs, pos, m, team):
    ls = [[] for _ in dirs]
    captures = []
    for dir in dirs:
        x = pos
        p = (x[0]+dir[0], x[1]+dir[1])
        while not m.isoccupied(p):
            ls[dirs.index(dir)].append(p)
            x = ls[dirs.index(dir)][-1]
            p = (x[0]+dir[0], x[1]+dir[1])
        if m.iscapturable(p, team):
            captures.append(p)
    return [sum(ls, []), captures]


def straightliners(looped, pos, m, team):
    ls = []
    captures = []
    for p in looped[0]:
        env = m.createEnv()
        env.move(pos, p)
        if not env.isvulnerable(env.getKingPos(team), team):
            ls.append(p)
        del env
    for p in looped[1]:
        env = m.createEnv()
        env.move(pos, p)
        if not env.isvulnerable(env.getKingPos(team), team):
            captures.append(p)
        del env
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
                if not m.isoccupied(p):
                    env = m.createEnv()
                    env.move(pos, p)
                    if not env.isvulnerable(p, self.team):
                        ls.append(p)
                    del env
                elif m.iscapturable(p, self.team):
                    env = m.createEnv()
                    env.move(pos, p)
                    if not env.isvulnerable(p, self.team):
                        captures.append(p)
                    del env

        return [ls, captures]
        # TODO: missing castling implementation


class Queen(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (1, -1), (-1, -1), (-1, 1)]
        looped = dirsLoop(dirs, pos, m, self.team)
        return straightliners(looped, pos, m, self.team)


class Rook(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        looped = dirsLoop(dirs, pos, m, self.team)
        return straightliners(looped, pos, m, self.team)


class Bishop(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        looped = dirsLoop(dirs, pos, m, self.team)
        return straightliners(looped, pos, m, self.team)


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
                env = m.createEnv()
                env.move(pos, p)
                if not env.isvulnerable(env.getKingPos(self.team), self.team):
                    ls.append(p)
                del env
            elif m.iscapturable(p, self.team):
                env = m.createEnv()
                env.move(pos, p)
                if not env.isvulnerable(env.getKingPos(self.team), self.team):
                    captures.append(p)
                del env

        return [ls, captures]


class Pawn(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        ls = []
        captures = []

        d = {True: -1, False: 1}[self.team]

        oneblock = (pos[0], pos[1] + d)
        if not m.isoccupied(oneblock):
            env = m.createEnv()
            env.move(pos, oneblock)
            if not env.isvulnerable(env.getKingPos(self.team), self.team):
                ls.append(oneblock)
            del env

        twoblocks = (pos[0], pos[1] + 2 * d)
        if pos[1] == 3.5 - 2.5 * d and not m.isoccupied(oneblock) and not m.isoccupied(twoblocks):
            env = m.createEnv()
            env.move(pos, twoblocks)
            if not env.isvulnerable(env.getKingPos(self.team), self.team):
                ls.append(twoblocks)
            del env

        for x in [1, -1]:
            p = (pos[0] + x, pos[1] + d)
            if m.iscapturable(p, self.team):
                env = m.createEnv()
                env.move(pos, p)
                if not env.isvulnerable(env.getKingPos(self.team), self.team):
                    captures.append(p)
                del env

        return [ls, captures]
        # TODO: missing en passant implementation
        # TODO: missing promotion implementation
