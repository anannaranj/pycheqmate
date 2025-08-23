import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    width: 450
    height: 450
    visible: true
    title: "Pycheqmate"
    Rectangle {
        height: Math.min(parent.height * 0.8, parent.width * 0.8)
        width: Math.min(parent.height * 0.8, parent.width * 0.8)
        color: "transparent"
        anchors {
            centerIn: parent
        }
        Grid {
            id: board
            anchors {
                horizontalCenter: parent.horizontalCenter
            }
            columns: 8
            rows: 8
            Repeater {
                id: cells
                model: 64
                Rectangle {
                    property string piece
                    property string cell
                    width: parent.parent.width * 1 / 9
                    height: parent.parent.height * 1 / 9
                    cell: "ABCDEFGH".split('')[index % 8] + (8 - Math.floor(index / 8))
                    // Average Javascript code be like:
                    color: Math.floor(index / 8) & 1 ? index & 1 ? "#ddd" : "#333" : index & 1 ? "#333" : "#ddd"
                    Component {
                        id: img
                        Image {
                            source: `../assets/${parent.parent.piece === parent.parent.piece.toUpperCase() ? parent.parent.piece + "w" : parent.parent.piece + "b"}.png`
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
        Rectangle {
            height: parent.height * 1 / 9
            width: parent.width * 8 / 9
            color: "transparent"
            anchors {
                horizontalCenter: parent.horizontalCenter
                top: board.bottom
            }
            FontLoader {
                id: freeserif
                source: "../assets/freeserif.ttf"
            }
            Label {
                id: turn
                height: parent.height
                width: parent.width
                text: "White's turn"
                fontSizeMode: Text.VerticalFit
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.family: freeserif.font.family
                font.pixelSize: 999
            }
            Row {
                id: whitePromoteMenu
                anchors {
                    centerIn: parent
                }
                height: parent.height
                width: parent.height * 4
                Repeater {
                    model: 4
                    Image {
                        property string piece: ["Q", "R", "B", "N"][index]
                        source: `../assets/${piece === piece.toUpperCase() ? piece + "w" : piece + "b"}.png`
                        height: parent.parent.height
                        width: parent.parent.height
                        mipmap: true
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                bridge.promote(parent.piece);
                            }
                        }
                    }
                }
                visible: false
            }
            Row {
                id: blackPromoteMenu
                anchors {
                    centerIn: parent
                }
                height: parent.height
                width: parent.height * 4
                Repeater {
                    model: 4
                    Image {
                        property string piece: ["q", "r", "b", "n"][index]
                        source: `../assets/${piece === piece.toUpperCase() ? piece + "w" : piece + "b"}.png`
                        height: parent.parent.height
                        width: parent.parent.height
                        mipmap: true
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                bridge.promote(parent.piece);
                            }
                        }
                    }
                }
                visible: false
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
        function onChangeText(text) {
            turn.text = text;
        }
        function onPromoteMenu(team) {
            if (team == "True") {
                whitePromoteMenu.visible = true;
                turn.visible = false;
            } else if (team == "False") {
                blackPromoteMenu.visible = true;
                turn.visible = false;
            } else {
                whitePromoteMenu.visible = false;
                blackPromoteMenu.visible = false;
                turn.visible = true;
            }
        }
    }
}
