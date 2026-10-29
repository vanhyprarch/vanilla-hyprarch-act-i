// SPDX-License-Identifier: GPL-2.0-only
import QtQuick
import Quickshell

ShellRoot {
  FloatingWindow {
    title: "Vanilla HyprArch Act I"
    implicitWidth: 1280
    implicitHeight: 720
    color: "#090e15"
    fullscreen: true
    Home { anchors.fill: parent; focus: true }
  }
}
