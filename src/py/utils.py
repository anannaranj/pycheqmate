# tuple (x, y)
def posToNotation(pos):
    return "ABCDEFGH"[pos[1]] + str(8-pos[0])


# Notation Eg. E4
def notationToPos(notation):
    return (8-int(notation[1]), "ABCDEFGH".index(notation[0]))
