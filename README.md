# Vanilla HyprArch Act I

A minimal, controller-first home theater environment built on vanilla Arch Linux,
Hyprland and Quickshell. Act I has its own repository and release cycle.

The first release targets Jellyfin MPV Shim and Moonlight. Steam is future scope;
Plex and Plex HTPC are out of scope. This project is an HTPC shell around desktop
applications, not a standalone Linux distribution.

## Current status

M1 is complete; M2 is in progress. A fullscreen Quickshell Home supports keyboard
selection and setup feedback for Jellyfin and Moonlight. The manual Hyprland
session uses its own repository configuration and includes a console-exit binding.
Keyboard behavior tests and an offscreen Quickshell load check pass. The owner
confirmed physical Home display, keyboard navigation, console exit/restart and
basic HDMI stereo output. Approved automatic startup through greetd, exit to
the text greeter and manual recovery have also been verified after reboot.

M2 is in progress: Home navigation is physically verified with a GuliKit KK3 Max
in Switch mode over Bluetooth. A five-second Home hold is physically verified
from the Jellyfin library. See [gamepad behavior](docs/gamepad.md) and the explicit
[Flatpak installer](docs/applications.md). Jellyfin library browsing, tile re-entry, cold launch and return on close are
verified on the target. Workspace switching now preserves a film detail page,
with Home + D-pad left/right shortcuts and focus-isolated Jellyfin input.
See [workspace controls](docs/workspace-navigation.md). HDR and refresh switching
remain planned. Moonlight testing is deferred
until a Sunshine host is available. See [manual session usage](docs/manual-session.md).

All source, Git operations, builds and runtime tests belong on the dedicated test
machine. The production workstation is an SSH client only and must not contain
a project checkout. Development-machine maintenance records stay outside this
repository.

## Planned components

- **Home:** a TV-friendly Quickshell launcher, with keyboard navigation first and
  Xbox/PlayStation controller navigation next.
- **Session manager:** application lifecycle, fullscreen workspaces, focus, Home
  navigation, controller routing and background audio policy.
- **Display manager:** supported refresh-rate selection, per-session display
  requests, Home-mode restoration and time-bounded recovery.
- **Application adapters:** separate MPV/Jellyfin and Moonlight integrations.

Start with one output and one seat. Separate HDR policy from refresh selection.
Do not claim HDR, refresh matching or controller compatibility before hardware
validation. Jellyfin MPV Shim 3.x includes an MPV library browser and gamepad input;
its suitability still needs hardware validation.

## Repository layout

| Directory | Purpose |
| --- | --- |
| `docs/` | Architecture, baseline, milestones and operating instructions |
| `shell/` | Quickshell Home launcher |
| `services/` | Session and display managers |
| `adapters/` | Application-specific integrations |
| `config/` | Reviewed configuration templates |
| `scripts/` | Setup, diagnostics and recovery |
| `tests/` | Automated checks and hardware validation guidance |

Read [architecture](docs/architecture.md), [milestones](docs/milestones.md),
[hardware baseline](docs/hardware-baseline.md),
[display baseline](docs/display-baseline.md) and
[remote workflow](docs/remote-workflow.md) before development.

## Development rules

Keep changes small, modular and maintainable. Use upstream packages when suitable.
Record the exact software versions and hardware test results. System changes,
reboots during testing, external publication and destructive operations need the
owner's authorization. Never use unrestricted root SSH or broad passwordless sudo.

Repository prose, source comments and commit messages are written in English.
Do not commit credentials, SSH material or personal network configuration.

## License

GNU General Public License, version 2 only (`GPL-2.0-only`). See [LICENSE](LICENSE).
This project does not grant an option to use a later GPL version.
