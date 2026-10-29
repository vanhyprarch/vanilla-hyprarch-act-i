# Development milestones

Each milestone uses small commits and records versions, exact tests, results and
open issues. Stop for owner decisions when tradeoffs affect the design.

## M0: Remote access and baseline

- [x] Verify non-root SSH from Codex and physical-console host-key trust.
- [x] Verify direct remote file editing and cleanup.
- [x] Inspect hardware and the installed base system.
- [x] Approve repository structure and GPL-2.0-only licensing.
- [x] Install Git and libdisplay-info after owner approval.
- [x] Decode the TV EDID and document remaining limits and the conformance warning.
- [x] Initialize Git on T8 using branch `main`.
- [x] Create the first baseline commit using owner-confirmed author details.
- [x] Verify password-protected sudo through the approved package installation.
- [x] Connect a separate public GitHub repository and verify matching local/remote commits.

## M1: Minimal graphical appliance

Status: initial milestone complete.

Install a reviewed Hyprland, Quickshell and audio baseline on T8. Provide a simple
Home with keyboard navigation, a dedicated local session and a console recovery
path. Add automatic login and reboot testing only with explicit authorization.

Progress:
- [x] Implement the keyboard-first Home, manual session scripts and isolated config.
- [x] Validate keyboard behavior, offscreen shell loading and config syntax.
- [x] Verify manual Home display, keyboard input, basic HDMI audio and console recovery.
- [x] Implement and test approved automatic login and boot recovery using greetd.

Acceptance: Home appears reliably after approved boot testing; a failed graphical
startup has a documented recovery path. Keep this sprint focused on the shell.

## M2: Controller-first shell

Verify Xbox/PlayStation Home navigation, application launch, fullscreen workspaces,
Home/app switching and return on exit. Select and validate a gamepad-friendly
Jellyfin browsing frontend rather than silently depending on phone casting.

Progress:
- [x] Verify KK3 Max Switch-mode Bluetooth Home navigation.
- [x] Verify Jellyfin MPV Shim 3.3.0 library browsing and gamepad navigation.
- [x] Verify repeated workspace changes with Home held, and no action from Home alone.
- [x] Accept Jellyfin tile launch, fullscreen re-entry and close/recovery.
- [x] Preserve film detail pages across Home/tile and Home+D-pad transitions.
- [x] Verify native Jellyfin controls still work after re-entry.
- [ ] Verify Bluetooth disconnect/reconnect and additional controller families.
- [ ] Validate Moonlight when a Sunshine host is available.

The first hardware test uses a Nintendo-mode controller. Xbox/PlayStation and
Moonlight remain pending; M2 is not complete. Face-button consistency is an open
owner decision; preserve the existing Jellyfin mapping until it is resolved.

## M3: Media playback and HDR

Validate Jellyfin/MPV with SDR, HDR, return to SDR, subtitles and representative
1080p/4K media. Confirm the display path, not only player metadata.

## M4: Refresh manager

Test supported exact/integer-multiple matching for fractional and integer video
rates, active-workspace changes, preferred-mode restoration and bounded fallback.
Verify actual display mode, playback statistics, blackouts and audio resync.

## M5: Moonlight session management

Verify controller passthrough and 1080p/4K streaming at supported rates. Test Home
switching, session preservation and background audio. Investigate safe pause
semantics without assuming remote games support them.

## M6: Reproducible release

Provide idempotent setup/update scripts, configuration, rollback/uninstall and
concise documentation. An ISO is not required for the initial release.
