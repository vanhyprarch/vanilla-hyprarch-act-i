# Services

`session/gamepad.py` implements the first unprivileged input bridge owned by the
Quickshell Home. It uses evdev and pyudev, gates normal actions by window focus,
and handles repeated Home-modified D-pad clicks without timed Home actions. See
[gamepad input](../docs/gamepad.md).

`session/application.py` manages one reviewed application through Hyprland IPC
events and a small injected adapter. Quickshell owns its command pipe; Home reload
does not terminate the app. The first implemented adapter is Jellyfin. See
[application behavior](../docs/applications.md).

Display management and Moonlight integration remain planned. Preserve the
separation between application adapters and shared session policy.
