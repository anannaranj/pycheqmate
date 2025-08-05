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
    # a simple variable that is the index of the first move in history
    # reason being is to detect if it is possible to castle now
    firstMove = None

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
    # a simple variable that is the index of the first move in history
    # reason being is to detect if it is possible to castle now
    firstMove = None

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
    # a simple variable that is the index of the first move in history
    # reason being is to detect if it is possible to EN PASSANT
    firstMove = None
    # and btw.. if you didn't understand that word:
    """

+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                               oooo                                                                                                         .     |
|                                               `888                                                                                                       .o8     |
|      .oooooooo  .ooooo.   .ooooo.   .oooooooo  888   .ooooo.      .ooooo.  ooo. .oo.      oo.ooooo.   .oooo.    .oooo.o  .oooo.o  .oooo.   ooo. .oo.   .o888oo   |
|     888' `88b  d88' `88b d88' `88b 888' `88b   888  d88' `88b    d88' `88b `888P"Y88b      888' `88b `P  )88b  d88(  "8 d88(  "8 `P  )88b  `888P"Y88b    888     |
|     888   888  888   888 888   888 888   888   888  888ooo888    888ooo888  888   888      888   888  .oP"888  `"Y88b.  `"Y88b.   .oP"888   888   888    888     |
|     `88bod8P'  888   888 888   888 `88bod8P'   888  888    .o    888    .o  888   888      888   888 d8(  888  o.  )88b o.  )88b d8(  888   888   888    888 .   |
|     `8oooooo.  `Y8bod8P' `Y8bod8P' `8oooooo.  o888o `Y8bod8P'    `Y8bod8P' o888o o888o     888bod8P' `Y888""8o 8""888P' 8""888P' `Y888""8o o888o o888o   "888"   |
|     d"     YD                      d"     YD                                               888                                                                   |
|     "Y88888P'                      "Y88888P'                                              o888o                                                                  |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------+

    """

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
