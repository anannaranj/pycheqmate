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

    @Slot()
    def loadBoard(self):
        g[0] = Game("src/csv/rooks.csv")
        x = "".join(["".join(i) for i in g[0].board.hmap])
        self.boardLoaded.emit(x)

    @Slot(str)
    def handleClick(self, cell):
        pos = notationToPos(cell)
        print(g[0].board.hmap[pos])


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    bridgeObj = Bridge()
    engine.rootContext().setContextProperty("bridge", bridgeObj)

    engine.load(QUrl(str(Path(__file__).parent) + "/Root/main.qml"))

    print(g[0])
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
