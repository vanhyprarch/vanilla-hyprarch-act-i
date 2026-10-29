// SPDX-License-Identifier: GPL-2.0-only
import QtQuick
import QtQuick.Window
import Quickshell
import Quickshell.Io

ShellRoot {
  id: root
  readonly property bool homeFocused: home.Window.active
  onHomeFocusedChanged: sendFocus()
  function sendFocus() {
    if (gamepad.running) {
      gamepad.write(JSON.stringify({type: "focus", focused: root.homeFocused}) + "\n");
    }
  }
  Process {
    id: gamepad
    command: [Quickshell.env("ACT_I_REPO_DIR") + "/scripts/gamepad-events"]
    stdinEnabled: true
    running: true
    onStarted: root.sendFocus()
    stdout: SplitParser {
      onRead: data => {
        try {
          const message = JSON.parse(data);
          if (message.type === "devices") home.gamepadCount = message.count;
          else if (message.type === "action") {
            if (message.action === "home") returnHome.running = true;
            else if (root.homeFocused) home.navigate(message.action);
          }
        } catch (error) { console.warn("Invalid gamepad event:", error); }
      }
    }
    stderr: SplitParser { onRead: data => console.warn(data) }
    onExited: (exitCode, exitStatus) => {
      home.gamepadCount = 0;
      console.warn("Gamepad reader stopped:", exitCode);
    }
  }
  Process {
    id: returnHome
    command: ["hyprctl", "dispatch", "hl.dsp.focus({workspace=1})"]
    stdout: StdioCollector {}
    stderr: SplitParser { onRead: data => console.warn(data) }
  }
  FloatingWindow {
    id: homeWindow
    title: "Vanilla HyprArch Act I"
    implicitWidth: 1280
    implicitHeight: 720
    color: "#090e15"
    fullscreen: true
    Home { id: home; anchors.fill: parent; focus: true }
  }
}
