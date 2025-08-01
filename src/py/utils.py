# tuple (x, y)
def posToNotation(pos):
    return "ABCDEFGH"[pos[0]] + str(8-pos[1])


# Notation Eg. E4
def notationToPos(notation):
    return ("ABCDEFGH".index(notation[0]), 8-int(notation[1]))
