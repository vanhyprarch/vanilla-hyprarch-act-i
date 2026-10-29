# M1 manual Home session

This first increment provides a fullscreen keyboard-navigable Home. Jellyfin and
Moonlight tiles show setup feedback; application launch and gamepad input are M2
work. No automatic login, display-rate manager or HDR switching is implemented.

## Runtime packages

Use the official Arch packages `hyprland`, `quickshell`, `pipewire`,
`pipewire-audio`, `pipewire-pulse`, `wireplumber`, `rtkit` and `ttf-dejavu`.
This config targets Hyprland 0.57 (Lua) and Quickshell 0.3.2. Required graphics
and media drivers depend on the target GPU and are outside the launcher itself.

## Start on the target

Log into a local text console as the normal HTPC user, then run:

```sh
cd ~/Projects/vanilla-hyprarch-act-i
./scripts/start-session
```

The script uses the configuration directly from this checkout. It does not copy
or replace `~/.config/hypr` or `~/.config/quickshell`. The initial output uses its
preferred mode with SDR color management. Real output-mode validation is pending.

Set an explicit XKB layout when needed, for example:

```sh
ACT_I_KEYBOARD_LAYOUT=it ./scripts/start-session
```

## Controls and recovery

| Key | Action |
| --- | --- |
| Arrows or Tab / Shift+Tab | Move selection |
| Enter or Space | Show the selected application's setup status |
| Esc | Dismiss the setup message |
| Super+H | Focus Home workspace 1 |
| Super+R | Request Home startup again if it has exited |
| Super+Shift+E | End the compositor session and return to the console |

If the graphical session is unresponsive, use Ctrl+Alt+F2 to reach another text
console. Authorized SSH access remains available for diagnosis. As the same user,
`hyprctl instances` identifies compositor instances; use the matching instance
explicitly when ending a session. Never terminate unrelated compositor instances.

## Checks

Run navigation tests on the target without a desktop:

```sh
QT_QPA_PLATFORM=offscreen /usr/lib/qt6/bin/qmltestrunner -input tests -o -,txt
```

Hardware acceptance still requires a physical session: visible Home, keyboard
navigation, legible TV sizing, confirmed SDR output, session exit/recovery and audio
routing. Autologin follows only after that acceptance and owner authorization.

Keep development-machine preparation and raw diagnostic records outside this
repository. This document describes the project's implementation and usage only.
