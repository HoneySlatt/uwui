import QtQuick
import QtQuick.Controls

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")

    Column {
        anchors.centerIn: parent
        spacing: 8

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Hello, World!"
        }

        Button {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Let's Go!"
            highlighted: true
            onClicked: console.log("Clicked!")
        }
    }
}
