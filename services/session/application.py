# SPDX-License-Identifier: GPL-2.0-only
"""A single application lifecycle, driven by Hyprland IPC events."""
import json
import os
from pathlib import Path
import selectors
import socket
import subprocess
import sys
import time



class Hyprland:
    def __init__(self):
        self.signature = os.environ["HYPRLAND_INSTANCE_SIGNATURE"]
        self.directory = Path(os.environ["XDG_RUNTIME_DIR"]) / "hypr" / self.signature

    def query(self, name):
        result = subprocess.run(["hyprctl", "-i", self.signature, "-j", name],
                                check=True, capture_output=True, text=True, timeout=5)
        return json.loads(result.stdout)

    def dispatch(self, expression):
        result = subprocess.run(["hyprctl", "-i", self.signature, "dispatch", expression],
                                check=True, capture_output=True, text=True, timeout=5)
        if result.stdout.strip() != "ok":
            raise RuntimeError("Hyprland rejected application action: " + result.stdout.strip())

    def home_if_active(self, workspace):
        if self.query("activeworkspace").get("id") == workspace:
            self.dispatch("hl.dsp.focus({workspace=1})")


class ApplicationSession:
    def __init__(self, app, hyprland, adapter):
        self.app = app
        self.adapter = adapter
        self.hyprland = hyprland
        self.seen_window = False

    def windows(self):
        return [c for c in self.hyprland.query("clients")
                if c.get("class") == self.adapter.WINDOW_CLASS and c.get("mapped")]

    def focus(self):
        self.hyprland.dispatch(f"hl.dsp.focus({{workspace={self.app.workspace}}})")
        for window in self.windows():
            if window.get("fullscreen") != 2:
                selector = json.dumps("address:" + window["address"])
                self.hyprland.dispatch("hl.dsp.window.fullscreen_state({window=" + selector
                                       + ',action="set",internal=2,client=0})')
        windows = self.windows()
        if windows:
            selector = json.dumps("address:" + windows[0]["address"])
            self.hyprland.dispatch("hl.dsp.focus({window=" + selector + "})")

    def refresh(self):
        windows = self.windows()
        if windows:
            self.seen_window = True
        elif self.seen_window:
            self.hyprland.home_if_active(self.app.workspace)
            return False
        return True

    def run(self):
        events = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        events.connect(str(self.hyprland.directory / ".socket2.sock"))
        events.setblocking(False)
        selector = selectors.DefaultSelector()
        selector.register(events, selectors.EVENT_READ, "events")
        selector.register(sys.stdin, selectors.EVENT_READ, "commands")
        child = None
        child_fd = None
        log = None
        buffer = b""
        commands = b""
        deadline = time.monotonic() + 30
        try:
            if not self.windows():
                self.adapter.prepare_profile(self.app.flatpak_id)
                state = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
                logs = state / "vanilla-hyprarch-act-i/applications"
                logs.mkdir(parents=True, exist_ok=True, mode=0o700)
                path = logs / (self.app.id + ".log")
                fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
                log = os.fdopen(fd, "a")
                child = subprocess.Popen(["flatpak", "--user", "run", self.app.flatpak_id],
                                         stdout=log, stderr=subprocess.STDOUT)
                child_fd = os.pidfd_open(child.pid)
                selector.register(child_fd, selectors.EVENT_READ, "child")
            self.focus()
            self.refresh()
            print(json.dumps({"state": "running"}), flush=True)
            while True:
                if not self.seen_window and time.monotonic() >= deadline:
                    raise RuntimeError(self.app.name + " did not open a window within 30 seconds")
                timeout = None if self.seen_window else max(0, deadline - time.monotonic())
                ready = selector.select(timeout)
                if not ready and not self.seen_window:
                    raise RuntimeError(self.app.name + " did not open a window within 30 seconds")
                for key, _ in ready:
                    if key.data == "commands":
                        data = os.read(sys.stdin.fileno(), 4096)
                        if not data:
                            return 0  # Home can restart without terminating the application.
                        commands += data
                        if len(commands) > 4096:
                            raise ValueError("Application command exceeds limit")
                        while b"\n" in commands:
                            line, commands = commands.split(b"\n", 1)
                            if line == b"focus":
                                self.focus()
                    elif key.data == "child":
                        selector.unregister(child_fd)
                        child.wait()
                        if not self.refresh():
                            return 0
                        if not self.seen_window:
                            raise RuntimeError(self.app.name + " exited before opening its window")
                    else:
                        data = events.recv(65536)
                        if not data:
                            return 0  # The compositor session ended.
                        buffer += data
                        while b"\n" in buffer:
                            line, buffer = buffer.split(b"\n", 1)
                            event = line.split(b">>", 1)[0]
                            if event in (b"openwindow", b"closewindow"):
                                if not self.refresh():
                                    return 0
        except Exception:
            self.hyprland.home_if_active(self.app.workspace)
            raise
        finally:
            selector.close()
            events.close()
            if child_fd is not None:
                os.close(child_fd)
            if log:
                log.close()
