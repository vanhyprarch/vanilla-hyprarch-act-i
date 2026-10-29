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
