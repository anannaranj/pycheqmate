import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Signal, Slot
from pathlib import Path
from py.game import Game


class Bridge(QObject):
    def __init__(self):
        QObject.__init__(self)

    loadBoardCalled = Signal(str, arguments=['map'])

    # @Slot()
    # def giveNumber(self):
    # self.nextNumber.emit(random.randint(0, 99))
    # print("hey")

    @Slot(str)
    def handleClick(self, cell):
        print(cell)

    @Slot(str)
    def loadBoard(self, line):
        self.loadBoardCalled.emit(line)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    bridgeObj = Bridge()
    engine.rootContext().setContextProperty("B", bridgeObj)

    engine.load(QUrl(str(Path(__file__).parent) + "/Root/main.qml"))

    g = Game("csv/rooks.csv")
    x = "".join(["".join(i) for i in g.board.hmap])

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
