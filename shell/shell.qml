// SPDX-License-Identifier: GPL-2.0-only
import QtQuick
import QtQuick.Window
import Quickshell
import Quickshell.Io

ShellRoot {
  id: root
  readonly property bool homeFocused: home.Window.active
  onHomeFocusedChanged: sendFocus()
  property var workspaceQueue: []
  property bool workspaceBusy: false
  function changeWorkspace(action) {
    workspaceQueue.push(action);
    runNextWorkspaceAction();
  }
  function runNextWorkspaceAction() {
    if (workspaceBusy || workspaceQueue.length === 0) return;
    workspaceBusy = true;
    const action = workspaceQueue.shift();
    workspaceAction.command = [Quickshell.env("ACT_I_REPO_DIR") + "/scripts/workspace-action", action];
    workspaceAction.running = true;
  }
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
            if (message.action === "app-next") root.changeWorkspace("next");
            else if (message.action === "app-previous") root.changeWorkspace("previous");
            else if (message.action === "app-close") root.changeWorkspace("close");
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
    id: workspaceAction
    onExited: (exitCode, exitStatus) => {
      if (exitCode !== 0) console.warn("Workspace action failed:", exitCode);
      root.workspaceBusy = false;
      Qt.callLater(root.runNextWorkspaceAction);
    }
    stdout: StdioCollector {}
    stderr: SplitParser { onRead: data => console.warn(data) }
  }
  Process {
    id: jellyfinCheck
    command: [Quickshell.env("ACT_I_REPO_DIR") + "/scripts/app-session", "jellyfin", "--check"]
    running: true
    stdout: SplitParser {
      onRead: data => {
        try { home.jellyfinAvailable = JSON.parse(data).installed === true; }
        catch (error) { console.warn("Invalid application status:", error); }
      }
    }
  }
  Process {
    id: jellyfinSession
    command: [Quickshell.env("ACT_I_REPO_DIR") + "/scripts/app-session", "jellyfin"]
    stdinEnabled: true
    stdout: SplitParser { onRead: data => {} }
    stderr: SplitParser { onRead: data => console.warn(data) }
    onExited: (exitCode, exitStatus) => {
      if (exitCode !== 0) home.notice = "Jellyfin could not start. Please try again.";
    }
  }
  FloatingWindow {
    id: homeWindow
    title: "Vanilla HyprArch Act I"
    implicitWidth: 1280
    implicitHeight: 720
    color: "#090e15"
    fullscreen: true
    Home {
      id: home
      anchors.fill: parent
      focus: true
      onLaunchRequested: application => {
        if (application === "jellyfin") {
          if (jellyfinSession.running) jellyfinSession.write("focus\n");
          else jellyfinSession.running = true;
        }
      }
    }
  }
}
