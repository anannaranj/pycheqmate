import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Signal, Slot
from pathlib import Path
from py.game import Game


g = None


class Bridge(QObject):
    def __init__(self):
        QObject.__init__(self)

    boardLoaded = Signal(str, arguments=['map'])

    @Slot(str)
    def handleClick(self, cell):
        print(cell)

    @Slot()
    def loadBoard(self):
        g = Game("csv/rooks.csv")
        x = "".join(["".join(i) for i in g.board.hmap])
        self.boardLoaded.emit(x)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    bridgeObj = Bridge()
    engine.rootContext().setContextProperty("bridge", bridgeObj)

    engine.load(QUrl(str(Path(__file__).parent) + "/Root/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
