# Services

`session/gamepad.py` implements the first unprivileged input bridge owned by the
Quickshell Home. It uses evdev and pyudev, gates normal actions by window focus,
and requests Home after a deliberate five-second Home-button hold. See
[gamepad input](../docs/gamepad.md).

Application lifecycle and display management remain separate planned increments.
Use Hyprland events and small application adapters rather than polling windows.
