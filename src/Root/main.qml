import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: window
    width: 450
    height: 450
    visible: true
    title: "Pycheqmate"
    ColumnLayout {
        height: Math.min(parent.height * 0.9, parent.width * 0.9)
        width: Math.min(parent.height * 0.9, parent.width * 0.9)
        anchors {
            centerIn: parent
        }
        Grid {
            columns: 8
            rows: 8
            Repeater {
                id: cells
                model: 64
                Rectangle {
                    required property int index
                    property string piece
                    property string cell
                    width: parent.parent.width * 0.125
                    height: parent.parent.width * 0.125
                    cell: "ABCDEFGH".split('')[index % 8] + (8 - Math.floor(index / 8))
                    // Average Javascript code be like:
                    color: Math.floor(index / 8) & 1 ? index & 1 ? "#ddd" : "#333" : index & 1 ? "#333" : "#ddd"
                    Component {
                        id: img
                        Image {
                            source: `../../assets/${parent.parent.piece}.png`
                            mipmap: true
                            anchors.centerIn: parent
                        }
                    }
                    Loader {
                        anchors.fill: parent
                        sourceComponent: img
                        active: parent.piece
                    }
                    Component {
                        id: empty
                        Item {}
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            bridge.handleClick(parent.cell);
                        }
                    }
                }
            }
        }
    }
    Component.onCompleted: {
        bridge.loadBoard();
    }
    Connections {
        target: bridge
        function onBoardLoaded(map) {
            map.split("").forEach((el, i) => {
                cells.itemAt(i).piece = el == "." ? null : el;
            });
        }
        function onHighlight(highlights) {
            highlights.forEach(el => {
                let index = el[1] * 8 + el[0];
                cells.itemAt(index).color = Math.floor(index / 8) & 1 ? index & 1 ? "#e7dea2" : "#a79f62" : index & 1 ? "#a79f62" : "#e7dea2";
            });
        }
        function onCaptureshighlight(captures) {
            captures.forEach(el => {
                let index = el[1] * 8 + el[0];
                cells.itemAt(index).color = Math.floor(index / 8) & 1 ? index & 1 ? "#cf6363" : "#922626" : index & 1 ? "#922626" : "#cf6363";
            });
        }
        function onHighlightreset(highlights) {
            for (let index = 0; index < 64; index++) {
                cells.itemAt(index).color = Math.floor(index / 8) & 1 ? index & 1 ? "#ddd" : "#333" : index & 1 ? "#333" : "#ddd";
            }
        }
    }
}
