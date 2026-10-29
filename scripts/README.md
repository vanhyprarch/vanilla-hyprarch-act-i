# Scripts

All scripts run as the normal HTPC user on the dedicated target.

- `start-session`: start the isolated Hyprland session from a local console.
- `start-home`: launch the Quickshell configuration from this checkout.
- `gamepad-events`: private focus-aware input bridge owned by Quickshell.
- `install-apps`: explicitly install selected reviewed per-user Flatpaks.
- `workspace-action`: focus Home or cycle already-open application workspaces.
- `app-session`: launch/restore Jellyfin and observe window lifecycle through IPC.

See [session usage](../docs/manual-session.md), [gamepad behavior](../docs/gamepad.md)
and [applications](../docs/applications.md). Full-system installation and an
optional-application selection UI remain later work.
