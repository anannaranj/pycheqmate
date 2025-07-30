import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: win
    width: 800
    height: 600
    visible: true
    title: "Pycheqmate"
    Rectangle {
        color: "#663399"
        width: 300
        height: 200
        anchors {
            verticalCenter: parent.verticalCenter
            horizontalCenter: parent.horizontalCenter
        }
        Text {
            id: name
            text: "Yet another chess clone!"
            color: "white"
            font.pixelSize: 20
            anchors {
                verticalCenter: parent.verticalCenter
                horizontalCenter: parent.horizontalCenter
            }
        }
    }
}
