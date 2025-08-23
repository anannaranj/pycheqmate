# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --include-qt-plugins=qml
# nuitka-project: --standalone
# nuitka-project: --output-dir=../build

# nuitka-project: --include-data-dir=Root=Root
# nuitka-project: --include-data-files=./assets/freeserif.ttf=./assets/freeserif.ttf
# nuitka-project: --include-data-files=./assets/logo.png=./assets/logo.png
# nuitka-project: --include-data-files=./assets/K.png=./assets/K.png
# nuitka-project: --include-data-files=./assets/k.png=./assets/k.png
# nuitka-project: --include-data-files=./assets/Q.png=./assets/Q.png
# nuitka-project: --include-data-files=./assets/q.png=./assets/q.png
# nuitka-project: --include-data-files=./assets/R.png=./assets/R.png
# nuitka-project: --include-data-files=./assets/r.png=./assets/r.png
# nuitka-project: --include-data-files=./assets/N.png=./assets/N.png
# nuitka-project: --include-data-files=./assets/n.png=./assets/n.png
# nuitka-project: --include-data-files=./assets/B.png=./assets/B.png
# nuitka-project: --include-data-files=./assets/b.png=./assets/b.png
# nuitka-project: --include-data-files=./assets/P.png=./assets/P.png
# nuitka-project: --include-data-files=./assets/p.png=./assets/p.png

# nuitka-project: --linux-icon=./assets/logo.png
# nuitka-project: --windows-icon-from-ico=./assets/logo.png
# nuitka-project: --windows-console-mode=disable


import sys
import os
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Signal, Slot
from py.game import Game
# from py.utils import notationToPos, posToNotation
from py.utils import notationToPos

g = [None]


class Bridge(QObject):
    def __init__(self):
        QObject.__init__(self)

    boardLoaded = Signal(str, arguments=['map'])
    highlight = Signal(list, arguments=["highlights"])
    captureshighlight = Signal(list, arguments=["captures"])
    highlightreset = Signal()
    changeText = Signal(str, arguments=["text"])
    promoteMenu = Signal(str, arguments=["team"])
    promoteMenuPos = None
    game = False

    def handleTurn(self, team):
        x = "White's turn" if team else "Black's turn"

        if g[0].board.isvulnerable(g[0].board.getKingPos(team), team):
            self.changeText.emit(x + ": Checked")
        else:
            self.changeText.emit(x)
        foundMove = False
        for x in range(8):
            broken = False
            for y in range(8):
                pos = (x, y)
                if g[0].board.cmap[pos[::-1]] is not None:
                    if g[0].board.cmap[pos[::-1]].team == team:
                        if g[0].board.cmap[pos[::-1]].listMoves(pos, g[0].board) != [[], []]:
                            g[0].board.cmap[
                                pos[::-1]
                            ].listMoves(pos, g[0].board)
                            foundMove = True
                            broken = True
                            break
            if broken:
                break
        if not foundMove:
            if g[0].board.isvulnerable(g[0].board.getKingPos(team), team):
                self.changeText.emit(
                    f"{"Black" if team else "White"} Wins: Cheqmate!")
                self.game = True
            else:
                self.changeText.emit("Draw: Stalemate!")
                self.game = True

    @Slot()
    def loadBoard(self):
        if g[0] is None:
            # g[0] = Game("./csv/screenshot.csv")
            g[0] = Game()
        x = "".join(["".join(i) for i in g[0].board.hmap])
        self.boardLoaded.emit(x)

    @Slot(str)
    def handleClick(self, cell):
        if self.promoteMenuPos or self.game:
            return
        pos = notationToPos(cell)

        if g[0].lastMovesList[1] is not None and pos in g[0].lastMovesList[1]:
            # CAPTURES
            if g[0].board.cmap[pos[::-1]] is None:
                temp = g[0].board.cmap[(g[0].lastClickedPiece[::-1])]
                g[0].board.cmap[(
                    pos[1] + (1 if temp.team else -1), pos[0])] = None
                g[0].board.hmap[(
                    pos[1] + (1 if temp.team else -1), pos[0])] = "."
            x = g[0].move(g[0].lastClickedPiece, pos)
            if x is not None:
                self.promoteMenu.emit("True" if x == "P" else "False")
                self.promoteMenuPos = pos
            self.loadBoard()
            self.highlightreset.emit()
            self.handleTurn(not g[0].board.cmap[pos[::-1]].team)
            g[0].lastMovesList = [None, None, None]
        elif g[0].board.cmap[pos[::-1]] is not None:
            # UNHIGHLIGHTED PIECE
            if g[0].board.cmap[pos[::-1]].team != len(g[0].history) % 2:
                # HIGHLIGHT LEGAL MOVES
                specials = []
                if pos == (4, 7) and g[0].board.hmap[(7, 4)] == "K" and g[0].board.cmap[(7, 4)].firstMove is None:
                    if g[0].board.hmap[(7, 7)] == "R" and g[0].board.hmap[(7, 6)] == "." and g[0].board.hmap[(7, 5)] == "." and g[0].board.cmap[(7, 7)].firstMove is None and not g[0].board.isvulnerable((4, 7), True) and not g[0].board.isvulnerable((5, 7), True) and not g[0].board.isvulnerable((6, 7), True):

                        specials.append("O-O")
                    if g[0].board.hmap[(7, 0)] == "R" and g[0].board.hmap[(7, 1)] == "." and g[0].board.hmap[(7, 2)] == "." and g[0].board.hmap[(7, 3)] == "." and g[0].board.cmap[(7, 0)].firstMove is None and not g[0].board.isvulnerable((4, 7), True) and not g[0].board.isvulnerable((3, 7), True) and not g[0].board.isvulnerable((2, 7), True):
                        specials.append("O-O-O")
                if pos == (4, 0) and g[0].board.hmap[(0, 4)] == "k" and g[0].board.cmap[(0, 4)].firstMove is None:
                    if g[0].board.hmap[(0, 7)] == "r" and g[0].board.hmap[(0, 6)] == "." and g[0].board.hmap[(0, 5)] == "." and g[0].board.cmap[(0, 7)].firstMove is None and not g[0].board.isvulnerable((4, 0), False) and not g[0].board.isvulnerable((5, 0), False) and not g[0].board.isvulnerable((6, 0), False):
                        specials.append("o-o")
                    if g[0].board.hmap[(0, 0)] == "r" and g[0].board.hmap[(0, 1)] == "." and g[0].board.hmap[(0, 2)] == "." and g[0].board.hmap[(0, 3)] == "." and g[0].board.cmap[(0, 0)].firstMove is None and not g[0].board.isvulnerable((4, 0), False) and not g[0].board.isvulnerable((3, 0), False) and not g[0].board.isvulnerable((2, 0), False):
                        specials.append("o-o-o")

                moveslist = g[0].board.listMoves(pos)
                if specials == []:
                    specials = [None]
                if g[0].board.hmap[pos[::-1]] == "P" and pos[1] == 3:
                    for x in [1, -1]:
                        p = (pos[0] + x, 3)
                        if (g[0].board.isinbounds(p)
                            and g[0].board.isoccupied(p)
                            and g[0].board.iscapturable(p, g[0].board.cmap[pos[::-1]].team)
                            and g[0].board.hmap[p[::-1]] == 'p'
                                and g[0].board.cmap[p[::-1]].firstMove == len(g[0].history) - 1):
                            moveslist[1].append((p[0], p[1]-1))
                if g[0].board.hmap[pos[::-1]] == "p" and pos[1] == 4:
                    for x in [1, -1]:
                        p = (pos[0] + x, 4)
                        if (g[0].board.isinbounds(p)
                            and g[0].board.isoccupied(p)
                            and g[0].board.iscapturable(p, g[0].board.cmap[pos[::-1]].team)
                            and g[0].board.hmap[p[::-1]] == 'P'
                                and g[0].board.cmap[p[::-1]].firstMove == len(g[0].history) - 1):
                            moveslist[1].append((p[0], p[1]+1))
                g[0].lastMovesList = [*moveslist, specials]
                self.highlightreset.emit()
                castles = []
                if specials is not []:
                    if "O-O" in specials:
                        castles.append((6, 7))
                    if "O-O-O" in specials:
                        castles.append((2, 7))
                    if "o-o" in specials:
                        castles.append((6, 0))
                    if "o-o-o" in specials:
                        castles.append((2, 0))
                self.highlight.emit([list(v) for v in moveslist[0] + castles])
                self.captureshighlight.emit([list(v) for v in moveslist[1]])
            else:
                # NOT THAT TEAM'S TURN
                self.highlightreset.emit()
                g[0].lastMovesList = [None, None, None]

        else:
            # NORMAL MOVE
            if g[0].lastMovesList[0] is not None and pos in g[0].lastMovesList[0]:
                x = g[0].move(g[0].lastClickedPiece, pos)
                if x is not None:
                    self.promoteMenu.emit("True" if x == "P" else "False")
                    self.promoteMenuPos = pos
                self.loadBoard()
                self.handleTurn(not g[0].board.cmap[pos[::-1]].team)
            elif g[0].lastMovesList[2] is not None:
                if "O-O" in g[0].lastMovesList[2] and pos == (6, 7):
                    g[0].castle("O-O")
                    self.loadBoard()
                    self.handleTurn(False)
                if "o-o" in g[0].lastMovesList[2] and pos == (6, 0):
                    g[0].castle("o-o")
                    self.loadBoard()
                    self.handleTurn(True)
                if "O-O-O" in g[0].lastMovesList[2] and pos == (2, 7):
                    g[0].castle("O-O-O")
                    self.loadBoard()
                    self.handleTurn(False)
                if "o-o-o" in g[0].lastMovesList[2] and pos == (2, 0):
                    g[0].castle("o-o-o")
                    self.loadBoard()
                    self.handleTurn(True)
            self.highlightreset.emit()
            g[0].lastMovesList = [None, None, None]

        g[0].lastClickedPiece = pos

    @Slot(str)
    def promote(self, piece):
        g[0].promote(self.promoteMenuPos, piece)
        self.loadBoard()
        self.promoteMenu.emit("None")
        self.promoteMenuPos = None


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon("./assets/logo.png"))
    engine = QQmlApplicationEngine()

    bridgeObj = Bridge()
    engine.rootContext().setContextProperty("bridge", bridgeObj)

    engine.load(QUrl.fromLocalFile(os.path.join(
        os.path.dirname(__file__), "Root", "main.qml")))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
