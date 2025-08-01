# the piece class is just the fundamental methods and values for all the 6 pieces
class Piece():
    # the team is a boolean, True for white, False for black
    def __init__(self, team):
        self.team = team


class Rook(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        ls = [[], [], [], []]
        captures = []
        for dir in dirs:
            x = pos
            while not (m.isoccupied((x[0]+dir[0], x[1]+dir[1]))):
                ls[dirs.index(dir)].append((x[0] + dir[0], x[1] + dir[1]))
                x = ls[dirs.index(dir)][-1]
            if m.iscapturable((x[0]+dir[0], x[1]+dir[1]), self.team):
                captures.append((x[0]+dir[0], x[1]+dir[1]))
        return [sum(ls, []), captures]


class Bishop(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        ls = [[], [], [], []]
        captures = []
        for dir in dirs:
            x = pos
            while not (m.isoccupied((x[0]+dir[0], x[1]+dir[1]))):
                ls[dirs.index(dir)].append((x[0] + dir[0], x[1] + dir[1]))
                x = ls[dirs.index(dir)][-1]
            if m.iscapturable((x[0]+dir[0], x[1]+dir[1]), self.team):
                captures.append((x[0]+dir[0], x[1]+dir[1]))
        return [sum(ls, []), captures]


class Queen(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (1, -1), (-1, -1), (-1, 1)]
        ls = [[], [], [], [], [], [], [], []]
        captures = []
        for dir in dirs:
            x = pos
            while not (m.isoccupied((x[0]+dir[0], x[1]+dir[1]))):
                ls[dirs.index(dir)].append((x[0] + dir[0], x[1] + dir[1]))
                x = ls[dirs.index(dir)][-1]
            if m.iscapturable((x[0]+dir[0], x[1]+dir[1]), self.team):
                captures.append((x[0]+dir[0], x[1]+dir[1]))
        return [sum(ls, []), captures]


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
        return [ls, captures]
