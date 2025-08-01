import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: window
    width: 450
    height: 450
    visible: true
    title: "Pycheqmate"
    Rectangle {
        width: 410
        height: 410
        border.width: 5
        border.color: "#333"
        anchors {
            centerIn: parent
        }
        Grid {
            anchors {
                verticalCenter: parent.verticalCenter
                horizontalCenter: parent.horizontalCenter
            }
            columns: 8
            rows: 8
            spacing: 0
            Repeater {
                id: cells
                model: 64
                Rectangle {
                    required property int index
                    property string piece
                    property string cell
                    width: 50
                    height: 50
                    cell: "ABCDEFGH".split('')[index % 8] + (8 - Math.floor(index / 8))
                    // Average Javascript code be like:
                    color: Math.floor(index / 8) & 1 ? index & 1 ? "#ddd" : "#333" : index & 1 ? "#333" : "#ddd"
                    Component {
                        id: img
                        Image {
                            source: `../../assets/${parent.parent.piece}.png`
                            width: 50
                            height: 50
                            mipmap: true
                            anchors.centerIn: parent
                        }
                    }
                    Loader {
                        anchors.fill: parent
                        sourceComponent: parent.piece !== "." && img
                    }
                    Component {
                        id: empty
                        Item {}
                    }
                    Text {
                        text: `${parent.cell}`
                        // Also average Javascript code be like:
                        color: Math.floor(index / 8) & 1 ? !(index & 1) ? "#ddd" : "#333" : !(index & 1) ? "#333" : "#ddd"
                        anchors {
                            left: parent.left
                            leftMargin: 2
                            top: parent.top
                            topMargin: 2
                        }
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
                cells.itemAt(i).piece = el;
            });
        }
        function onHighlight(highlights) {
            highlights.forEach(el => {
                let index = el[1] * 8 + el[0];
                cells.itemAt(index).color = Math.floor(index / 8) & 1 ? index & 1 ? "#df4" : "#333" : index & 1 ? "#333" : "#df0";
            });
        }
        function onHighlightreset(highlights) {
            for (let index = 0; index < 64; index++) {
                cells.itemAt(index).color = Math.floor(index / 8) & 1 ? index & 1 ? "#ddd" : "#333" : index & 1 ? "#333" : "#ddd";
            }
        }
    }
}
