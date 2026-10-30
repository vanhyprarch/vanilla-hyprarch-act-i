# SPDX-License-Identifier: GPL-2.0-only
"""Keep managed windows focused and playback aware of actual workspace changes."""
import asyncio
import json
import subprocess
import sys


class DesktopMonitor:
    def __init__(self, hyprland, applications, workspace_changed):
        self.hyprland = hyprland
        self.applications = list(applications)
        self.workspace_changed = workspace_changed

    def refresh(self):
        current = self.hyprland.query('activeworkspace').get('id')
        if type(current) is not int or current < 1:
            raise RuntimeError('No active application workspace')
        # Playback policy must not depend on optional window-focus repair.
        self.workspace_changed(current)
        clients = self.hyprland.query('clients')
        active = self.hyprland.query('activewindow')
        candidates = [window for app in self.applications if app.workspace == current
                      for window in clients if window.get('mapped')
                      and window.get('class') == app.window_class
                      and window.get('workspace', {}).get('id') == current]
        # A valid dialog or another focused window on this workspace keeps focus.
        # Repair only an absent/stale focus, never switch to a background app.
        if candidates and (not active.get('address')
                           or active.get('workspace', {}).get('id') != current):
            window = min(candidates, key=lambda w: w.get('focusHistoryID', 100000))
            selector = json.dumps('address:' + window['address'])
            self.hyprland.dispatch('hl.dsp.focus({window=' + selector + '})')

    async def _watch(self):
        reader, writer = await asyncio.open_unix_connection(
            str(self.hyprland.directory / '.socket2.sock'))
        try:
            await asyncio.to_thread(self.refresh)
            while line := await reader.readline():
                kind = line.split(b'>>', 1)[0]
                if kind in (b'workspace', b'workspacev2', b'openwindow', b'closewindow',
                            b'activewindowv2', b'fullscreen'):
                    await asyncio.to_thread(self.refresh)
        finally:
            writer.close()
            await writer.wait_closed()

    async def run(self):
        # Hotplug can temporarily invalidate a query or close the event socket.
        # Reconnect and resample current state instead of silently losing pause.
        while True:
            try:
                await self._watch()
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
                print(f"Workspace monitor unavailable: {error}; retrying", file=sys.stderr, flush=True)
            else:
                print("Workspace event stream closed; reconnecting", file=sys.stderr, flush=True)
            await asyncio.sleep(1)
