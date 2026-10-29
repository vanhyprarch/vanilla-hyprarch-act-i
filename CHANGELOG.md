# Changelog

## Unreleased

- Establish the remote-only development workflow and initial repository layout.
- Record the T8 hardware baseline and unverified display/audio capabilities.
- Document the architecture and M0-M6 acceptance criteria.
- Select GPL-2.0-only licensing.

- Add a fullscreen keyboard-first Quickshell Home and isolated manual Hyprland
  session with console recovery bindings.
- Add Qt Quick tests for selection, focus and setup feedback.

Application adapters and the full-system installer remain planned.

- Install the approved Git and EDID diagnostic tooling on T8.
- Initialize the remote Git repository with branch `main`.
- Record the TV's advertised 4K120/HDR capabilities and EDID conformance warning;
  end-to-end operation remains unverified.
- Publish the baseline to the separate public GitHub repository directly from T8.
- Verify repository-scoped SSH authentication and matching local/remote commits.
- Verify manual Home display, keyboard navigation, console exit/restart and basic
  HDMI stereo output with owner-observed hardware checks.
- Add an unapplied greetd template for the next automatic-start increment.
- Start Hyprland through its official watchdog launcher, preserving the isolated
  project configuration and avoiding the direct-start warning.
- Verify approved greetd autologin after reboot and text-greeter recovery on exit.
- Complete the initial M1 milestone; application launch and gamepad input remain M2.

- Add an explicit per-user Flatpak installer backed by a reviewed application catalog.
- Add non-exclusive gamepad input with focus gating, hotplug discovery and repeat control.
- Verify KK3 Max Switch-mode Bluetooth Home navigation on the TV.
- Verify the owner-selected five-second Home hold from the Jellyfin library.
- Add event-driven Jellyfin tile launch, re-entry, fullscreen workspace assignment
  and automatic Home return on graceful close, preserving existing app preferences.
- Verify Jellyfin library navigation and retained login after a cold client launch.
- Leave the existing Jellyfin face-button convention unchanged; Home/Jellyfin
  consistency remains an owner decision. Moonlight tests await a Sunshine host.

- Add Home + D-pad left/right to cycle already-open application workspaces,
  skipping closed apps and canceling the long Home hold after a chord.
- Isolate Jellyfin's native SDL input in background workspaces and during reserved
  Home gestures through a managed MPV script, preserving existing A/B bindings.
- Verify film detail-page preservation through tile and shortcut re-entry,
  unchanged process identity, and normal native controls after return.
