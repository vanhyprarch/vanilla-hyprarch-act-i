# Reviewed applications

The initial catalog is `config/apps.json`. Install applications per user from
Flathub; never run the application installer with sudo.

```sh
./scripts/install-apps --list
./scripts/install-apps --dry-run jellyfin
./scripts/install-apps jellyfin
```

An empty invocation lists the catalog without installing anything. Names must be
explicit; unknown names are rejected before any command executes. The installer
adds the official Flathub remote if needed and installs only the selected IDs.
Moonlight is a separate explicit selection, not an implicit dependency of Jellyfin.

| Selection | Flatpak ID | Planned workspace |
| --- | --- | --- |
| `jellyfin` | `com.github.iwalton3.jellyfin-mpv-shim` | 2 |
| `moonlight` | `com.moonlight_stream.Moonlight` | 3 |

Jellyfin MPV Shim 3.x includes a library browser and gamepad input inside MPV.
Evaluate this upstream interface on the actual target before adding another
frontend. Installation of a Flatpak does not prove controller navigation,
hardware decoding, HDR or fullscreen workspace lifecycle.

Keep Jellyfin server URLs, authentication and per-user state in the application's
private configuration outside this repository. A curated optional-application UI
and reproducible full-system installation remain later milestones.

## Jellyfin session

The Jellyfin tile detects the installed per-user Flatpak. Selecting it starts
`scripts/app-session jellyfin` or requests focus from the existing session helper.
The helper subscribes to Hyprland's event socket before inspecting windows, adopts
an already-open Act I Jellyfin window, and starts the Flatpak only when needed.
It returns to Home when the last Jellyfin window closes while workspace 2 is active.
If another workspace is active, closing a background window does not steal focus.
An initial launch has a 30-second window timeout with a return-to-Home fallback.

The profile uses the application's private Flatpak configuration directory.
New profiles enable the upstream gamepad UI and fullscreen browser; existing
Jellyfin JSON preferences and credentials are preserved byte-for-byte by the
adapter. The profile also receives a managed MPV input guard and private local
IPC option; a conflicting existing IPC server is reported instead of overwritten. MPV's
`wayland-app-id=org.vanhyprarch.acti.jellyfin` identifies the managed window.
A conflicting existing MPV profile is reported instead of being overwritten.
Hyprland places that class on workspace 2. Jellyfin manages its native browser
and playback fullscreen state; Act I focuses the existing window without
suppressing or overriding the client's fullscreen requests. New profiles enable
both fullscreen preferences. The initial Moonlight tile remains setup feedback
while Sunshine testing is deferred.

Quickshell and the application helper communicate over private process pipes;
ordinary navigation is still routed only to the focused Home. Closing/reloading
the shell closes that pipe and lets the helper exit without killing Jellyfin.
Application logs stay under the user's XDG state directory, outside Git.

## Hardware acceptance

With Jellyfin MPV Shim 3.3.0, the owner successfully authenticated, opened the
library on the TV, and navigated using the KK3 Max D-pad and face buttons. In the
observed Jellyfin configuration, physical B (south) selects and A (east) goes back.
Keep this configuration unchanged for now. Home still uses A (east) to select and
B (south) to go back; a unified convention is an explicit later owner decision.
Home + D-pad left/right changes between the launcher and open app workspaces.
Home can stay held across repeated clicks; Home alone has no timed action.

Tile-driven re-entry and a cold launch after graceful client shutdown are now
owner-verified, including retained authentication. Hyprland reports workspace 2,
fullscreen state 2 and a 3840x2160 window on the target. Graceful shutdown removed
the app window and automatically restored workspace 1. Bluetooth reconnect still
needs an acceptance check.
This does not validate video playback, HDR, hardware decoding, refresh matching,
Moonlight input forwarding or remote-game Home-button behavior.

Workspace-only return now preserves a film detail page through both tile re-entry
and Home + D-pad right; Home + D-pad left and normal input after return also passed
owner-observed checks. See [workspace navigation](workspace-navigation.md) for the
input isolation fix and the remaining Moonlight limitations.
