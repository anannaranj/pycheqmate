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
        for dir in dirs:
            x = pos
            while not (m.isoccupied((x[0]+dir[0], x[1]+dir[1]))):
                ls[dirs.index(dir)].append((x[0] + dir[0], x[1] + dir[1]))
                x = ls[dirs.index(dir)][-1]
        return sum(ls, [])


class Pawn(Piece):
    def __init__(self, team):
        Piece.__init__(self, team)

    # pos is a tuple (x, y)
    # m is the board
    def listMoves(self, pos, m):
        ls = []
        # white
        if self.team:
            if not m.isoccupied((pos[0], pos[1]-1)):
                ls.append((pos[0], pos[1]-1))
            if pos[1] == 6 and not m.isoccupied((pos[0], pos[1]-1)) and not m.isoccupied((pos[0], pos[1]-2)):
                ls.append((pos[0], pos[1]-2))
        # black
        else:
            if not m.isoccupied((pos[0], pos[1]+1)):
                ls.append((pos[0], pos[1]+1))
            if pos[1] == 1 and not m.isoccupied((pos[0], pos[1]-1)) and not m.isoccupied((pos[0], pos[1]+2)):
                ls.append((pos[0], pos[1]+2))
        return ls
