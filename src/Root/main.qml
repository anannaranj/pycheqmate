import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: win
    width: 450
    height: 450
    visible: true
    title: "Pycheqmate"
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
                width: 50
                height: 50
                // Average Javascript code be like:
                color: Math.floor(index / 8) & 1 ? index & 1 ? "#ddd" : "#333" : index & 1 ? "#333" : "#ddd"
                Text {
                    // Also average Javascript code be like:
                    text: "ABCDEFGH".split('')[index % 8] + (8 - Math.floor(index / 8))
                    color: Math.floor(index / 8) & 1 ? !(index & 1) ? "#ddd" : "#333" : !(index & 1) ? "#333" : "#ddd"
                    anchors {
                        left: parent.left
                        leftMargin: 2
                        top: parent.top
                        topMargin: 2
                    }
                }
            }
        }
    }
}
