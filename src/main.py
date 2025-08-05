# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --enable-plugin=numpy
# nuitka-project: --include-qt-plugins=qml
# nuitka-project: --standalone
# nuitka-project: --output-dir=../build

# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/Root=Root
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/assets=assets
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/csv=csv

import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Signal, Slot
from pathlib import Path
from py.game import Game
from py.utils import notationToPos, posToNotation


g = [None]


class Bridge(QObject):
    def __init__(self):
        QObject.__init__(self)

    boardLoaded = Signal(str, arguments=['map'])
    highlight = Signal(list, arguments=["highlights"])
    captureshighlight = Signal(list, arguments=["captures"])
    highlightreset = Signal()
    switchTeam = Signal(bool, arguments=["team"])
    promoteMenu = Signal(str, arguments=["team"])
    promoteMenuPos = None

    @Slot()
    def loadBoard(self):
        if g[0] is None:
            # g[0] = Game("./csv/pinned.csv")
            g[0] = Game()
        x = "".join(["".join(i) for i in g[0].board.hmap])
        self.boardLoaded.emit(x)

    @Slot(str)
    def handleClick(self, cell):
        if self.promoteMenuPos:
            return
        pos = notationToPos(cell)

        if g[0].lastMovesList[1] is not None and pos in g[0].lastMovesList[1]:
            # CAPTURES
            x = g[0].move(g[0].lastClickedPiece, pos)
            if x is not None:
                self.promoteMenu.emit("True" if x == "P" else "False")
                self.promoteMenuPos = pos
            self.loadBoard()
            self.highlightreset.emit()
            self.switchTeam.emit(not g[0].board.cmap[pos[::-1]].team)
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
                self.switchTeam.emit(not g[0].board.cmap[pos[::-1]].team)
            elif g[0].lastMovesList[2] is not None:
                if "O-O" in g[0].lastMovesList[2] and pos == (6, 7):
                    g[0].castle("O-O")
                    self.loadBoard()
                    self.switchTeam.emit(False)
                if "o-o" in g[0].lastMovesList[2] and pos == (6, 0):
                    g[0].castle("o-o")
                    self.loadBoard()
                    self.switchTeam.emit(True)
                if "O-O-O" in g[0].lastMovesList[2] and pos == (2, 7):
                    g[0].castle("O-O-O")
                    self.loadBoard()
                    self.switchTeam.emit(False)
                if "o-o-o" in g[0].lastMovesList[2] and pos == (2, 0):
                    g[0].castle("o-o-o")
                    self.loadBoard()
                    self.switchTeam.emit(True)
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
    engine = QQmlApplicationEngine()

    bridgeObj = Bridge()
    engine.rootContext().setContextProperty("bridge", bridgeObj)

    engine.load(QUrl(str(Path(__file__).parent) + "/Root/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
