// SPDX-License-Identifier: GPL-2.0-only
import QtQuick
import QtQuick.Window
Window {
  visible: true
  visibility: Window.FullScreen
  title: "Act I generic close test"
  color: "#17232c"
  onClosing: Qt.quit()
  Text {
    anchors.centerIn: parent
    text: "Generic application close test\nHome + D-pad Down"
    color: "#f4f1e9"
    font.pixelSize: 36
    horizontalAlignment: Text.AlignHCenter
  }
}
