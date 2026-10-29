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

The script uses the official `start-hyprland` watchdog launcher and selects the
configuration directly from this checkout. It does not copy
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

## Validation status

The manual prototype has passed owner-observed physical checks for Home display,
arrow/Enter/Esc navigation, exit to the console, restart into Home and a short HDMI
stereo playback check. These results do not validate application playback, HDR,
refresh switching, gamepad input or automatic boot.

## Automatic startup

`config/greetd/config.toml.in` is a generic template. Render its placeholders
for the dedicated target; keep that machine-specific result outside the repository. It requires the official `greetd` and `greetd-agreety` packages.
The initial session runs the normal user's `scripts/start-session` once per boot.
When that session ends, the default text greeter provides conventional login to a
shell, allowing recovery without repeatedly relaunching a broken graphical session.

Activation requires owner authorization, a backup of the installed greetd config,
review of the packaged service VT conflict handling, and a boot test. Configure
only the dedicated target's username and absolute session command. Keep target-
specific rendered configs and maintenance backups outside the project repository.

If automatic startup must be rolled back from an authorized SSH session:

```sh
sudo systemctl disable --now greetd.service
sudo systemctl enable --now getty@tty1.service
```

Other local text consoles remain the recovery path. Never enable automatic login
on a production workstation while testing this template.

### Activation sequence

On the dedicated target, after authorization:

1. Install `greetd` and `greetd-agreety` from the official Arch repositories.
2. Back up the existing `/etc/greetd/config.toml` and record current service states.
3. Render the template with the normal HTPC account and absolute `start-session`
   command; install it root-owned with mode 0644 as `/etc/greetd/config.toml`.
4. Verify `greetd.service` and `getty@tty2.service` with
   `systemd-analyze --man=no verify greetd.service getty@tty2.service`.
5. Enable those two units for the next boot. The packaged greetd unit must include
   `Conflicts=getty@tty1.service`; leave the recovery tty2 available.
6. Reboot only when authorized, verify automatic Home startup, then verify that
   exiting Home reaches the text greeter and permits manual session recovery.

This initial implementation intentionally keeps startup linked to the development
checkout. Packaging and a stable installed session path belong to the release work.
