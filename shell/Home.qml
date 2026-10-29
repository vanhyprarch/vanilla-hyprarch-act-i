// SPDX-License-Identifier: GPL-2.0-only
import QtQuick

FocusScope {
  id: home
  focus: true
  property int selectedIndex: 0
  property string notice: ""
  property int gamepadCount: 0
  property bool jellyfinAvailable: false
  signal launchRequested(string application)
  readonly property real unit: Math.max(0.5, Math.min(width / 1280, height / 720))
  readonly property var applications: [
    { id: "jellyfin", name: "Jellyfin", subtitle: "Movies & series", glyph: "\u25b6", accent: "#83d5d1" },
    { id: "moonlight", name: "Moonlight", subtitle: "Play from your PC", glyph: "\u25c7", accent: "#b4b6f2" }
  ]

  function moveSelection(offset) {
    selectedIndex = (selectedIndex + offset + applications.length) % applications.length;
  }

  function activateSelected() {
    const application = applications[selectedIndex];
    if (application.id === "jellyfin" && jellyfinAvailable) launchRequested(application.id);
    else notice = application.name + " is not configured yet.";
  }

  function navigate(action) {
    if (notice.length > 0) {
      if (action === "select" || action === "back") notice = "";
      return;
    }
    if (action === "next") moveSelection(1);
    else if (action === "previous") moveSelection(-1);
    else if (action === "select") activateSelected();
  }

  Component.onCompleted: forceActiveFocus()
  Keys.onPressed: event => {
    if (notice.length > 0) {
      if ([Qt.Key_Escape, Qt.Key_Back, Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space].includes(event.key))
        notice = "";
      event.accepted = true;
      return;
    }
    switch (event.key) {
    case Qt.Key_Right:
    case Qt.Key_Down:
      moveSelection(1);
      break;
    case Qt.Key_Left:
    case Qt.Key_Up:
    case Qt.Key_Backtab:
      moveSelection(-1);
      break;
    case Qt.Key_Tab:
      moveSelection(event.modifiers & Qt.ShiftModifier ? -1 : 1);
      break;
    case Qt.Key_Return:
    case Qt.Key_Enter:
    case Qt.Key_Space:
      activateSelected();
      break;
    default:
      return;
    }
    event.accepted = true;
  }

  Rectangle {
    anchors.fill: parent
    gradient: Gradient {
      GradientStop { position: 0; color: "#17232c" }
      GradientStop { position: 1; color: "#090e15" }
    }
  }

  Column {
    anchors.left: parent.left
    anchors.top: parent.top
    anchors.margins: 72 * home.unit
    spacing: 10 * home.unit
    Text {
      text: "VANILLA HYPRARCH"
      color: "#9aadb8"
      font.family: "DejaVu Sans"
      font.pixelSize: 16 * home.unit
      font.letterSpacing: 4 * home.unit
    }
    Text {
      text: "Act I"
      color: "#f4f1e9"
      font.family: "DejaVu Sans"
      font.pixelSize: 56 * home.unit
      font.weight: Font.Light
    }
  }

  Row {
    anchors.centerIn: parent
    anchors.verticalCenterOffset: 24 * home.unit
    spacing: 28 * home.unit
    Repeater {
      model: home.applications
      delegate: Rectangle {
        id: tile
        required property int index
        required property var modelData
        readonly property bool selected: home.selectedIndex === index
        width: 430 * home.unit
        height: 280 * home.unit
        radius: 22 * home.unit
        color: selected ? "#233543" : "#16232e"
        border.width: selected ? 3 * home.unit : 1 * home.unit
        border.color: selected ? "#e8ca83" : "#30424e"
        Accessible.role: Accessible.Button
        Accessible.name: modelData.name
        Accessible.description: modelData.subtitle + (modelData.id === "jellyfin" && home.jellyfinAvailable ? ". Open." : ". Setup required.")
        Behavior on color { ColorAnimation { duration: 120 } }

        Column {
          anchors.left: parent.left
          anchors.right: parent.right
          anchors.top: parent.top
          anchors.margins: 32 * home.unit
          spacing: 14 * home.unit
          Text {
            text: tile.modelData.glyph
            color: tile.modelData.accent
            font.family: "DejaVu Sans"
            font.pixelSize: 52 * home.unit
          }
          Text {
            text: tile.modelData.name
            color: "#f4f1e9"
            font.family: "DejaVu Sans"
            font.pixelSize: 34 * home.unit
            font.weight: Font.DemiBold
          }
          Text {
            text: tile.modelData.subtitle
            color: "#b7c7d2"
            font.family: "DejaVu Sans"
            font.pixelSize: 19 * home.unit
          }
        }
        Text {
          anchors.left: parent.left
          anchors.bottom: parent.bottom
          anchors.margins: 32 * home.unit
          text: tile.modelData.id === "jellyfin" && home.jellyfinAvailable ? "Open" : "Setup required"
          color: "#91a7b7"
          font.family: "DejaVu Sans"
          font.pixelSize: 14 * home.unit
        }
        MouseArea {
          anchors.fill: parent
          onClicked: {
            home.forceActiveFocus();
            home.selectedIndex = tile.index;
            home.activateSelected();
          }
        }
      }
    }
  }

  Text {
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.bottom: parent.bottom
    anchors.bottomMargin: 54 * home.unit
    text: home.gamepadCount > 0
      ? "D-pad / Stick   Choose       A   Select       B   Back       Hold Home 5s"
      : "\u2190  \u2192   Choose       Enter   Select       Esc   Back"
    color: "#a7bbc9"
    font.family: "DejaVu Sans"
    font.pixelSize: 18 * home.unit
  }

  Rectangle {
    anchors.fill: parent
    visible: home.notice.length > 0
    color: "#d9090e15"
    MouseArea { anchors.fill: parent; onClicked: home.notice = "" }
    Rectangle {
      anchors.centerIn: parent
      width: 680 * home.unit
      height: 250 * home.unit
      radius: 22 * home.unit
      color: "#1d2d3a"
      border.color: "#526b7a"
      border.width: home.unit
      Column {
        anchors.centerIn: parent
        spacing: 22 * home.unit
        Text {
          anchors.horizontalCenter: parent.horizontalCenter
          text: "Setup required"
          color: "#f4f1e9"
          font.family: "DejaVu Sans"
          font.pixelSize: 30 * home.unit
        }
        Text {
          anchors.horizontalCenter: parent.horizontalCenter
          text: home.notice
          color: "#c8d5dd"
          font.family: "DejaVu Sans"
          font.pixelSize: 21 * home.unit
        }
        Text {
          anchors.horizontalCenter: parent.horizontalCenter
          text: home.gamepadCount > 0 ? "Press A or B to return" : "Press Enter or Esc to return"
          color: "#e8ca83"
          font.family: "DejaVu Sans"
          font.pixelSize: 17 * home.unit
        }
      }
    }
  }
}
