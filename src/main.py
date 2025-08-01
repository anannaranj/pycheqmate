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

    @Slot()
    def loadBoard(self):
        if g[0] is None:
            # g[0] = Game("src/csv/pawns.csv")
            g[0] = Game()
        x = "".join(["".join(i) for i in g[0].board.hmap])
        self.boardLoaded.emit(x)

    @Slot(str)
    def handleClick(self, cell):
        pos = notationToPos(cell)

        if g[0].lastMovesList[1] is not None and pos in g[0].lastMovesList[1]:
            g[0].move(g[0].lastClickedPiece, pos)
            self.loadBoard()
            self.highlightreset.emit()
            g[0].lastMovesList = [None, None]
        elif g[0].board.cmap[pos[::-1]] is not None:
            moveslist = g[0].board.listMoves(pos)
            g[0].lastMovesList = moveslist
            self.highlightreset.emit()
            self.highlight.emit([list(v) for v in moveslist[0]])
            self.captureshighlight.emit([list(v) for v in moveslist[1]])
        else:
            if g[0].lastMovesList[0] is not None and pos in g[0].lastMovesList[0]:
                g[0].move(g[0].lastClickedPiece, pos)
                self.loadBoard()
            self.highlightreset.emit()
            g[0].lastMovesList = [None, None]

        g[0].lastClickedPiece = pos


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    bridgeObj = Bridge()
    engine.rootContext().setContextProperty("bridge", bridgeObj)

    engine.load(QUrl(str(Path(__file__).parent) + "/Root/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
