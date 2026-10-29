# Architecture

Status: a keyboard-first Home and manual session prototype are implemented.
Session/display managers and application adapters remain planned.

## Platform

Vanilla Arch Linux, systemd, Hyprland, Quickshell and PipeWire/WirePlumber.
The initial target is one display and one local seat. Preserve a console recovery
path. Automatic login belongs to the dedicated HTPC session and is a later,
explicitly approved system change.

## Home and session management

Home occupies logical workspace 1. Each supported application gets a dedicated
fullscreen workspace. Returning Home need not terminate an application; an
application exit must return to Home reliably.

Use Hyprland IPC events where practical. Track application lifecycle and focus,
route controller input deliberately, and prevent unintended background audio.
Do not steal Moonlight gameplay input except for a deliberately chosen Home
shortcut. Remote-game pausing is an investigation, not a promised capability.

## Display management

Maintain a preferred Home mode and an application-specific display request. Only
one physical mode can be active on the output at a time. Preserve the chosen
resolution by default and prefer exact refresh matches or integer multiples,
including fractional rates where actually supported.

Use MPV IPC to observe playback and metadata. Account for unreliable frame-rate
metadata, variable frame rate and track changes. Debounce requests, avoid mode
thrashing, and restore the relevant Home/application mode after lifecycle events.

HDR/SDR policy and refresh-rate selection are separate concerns. Monitor EDID,
kernel modes, compositor behavior and real playback must all be checked. Provide
a last-known-good fallback, bounded recovery and an accessible safe-mode action.

## Adapters and implementation choices

Keep application-specific behavior behind a small explicit adapter interface.
Choose service implementation languages and input libraries after targeted
prototypes; no additional runtime or IPC framework is selected at this stage.

Jellyfin library browsing must work from the couch. Evaluate the frontend before
claiming a fully controller-only Jellyfin experience. Audio passthrough, Atmos,
DTS:X and universal remote-game pausing remain investigations.
