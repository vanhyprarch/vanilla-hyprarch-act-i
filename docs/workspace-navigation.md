# Workspace navigation and preserved application state

| Control | Behavior |
| --- | --- |
| Hold Home for five seconds | Focus the Act I Home on workspace 1 |
| Hold Home, then press D-pad left once | Focus the previous workspace (Home or an open app) |
| Hold Home, then press D-pad right once | Focus the next workspace (Home or an open app) |
| Select an application tile | Focus its existing window, or launch it if closed |

Release Home before another shortcut. One left/right combination fires per Home
press and cancels the five-second return for that press. The D-pad is deliberate;
stick drift must not trigger an application switch. The controller-only Home
navigation mapping is unchanged.

Home always participates in the cycle as workspace 1. Open applications follow
in workspace order. Closed or unmapped applications are skipped without being
launched; with none open, either direction stays on Home.

With only Jellyfin open, both directions toggle Home (1) and Jellyfin (2).
With Jellyfin and Moonlight open, right cycles 1 → 2 → 3 → 1, while left cycles
1 → 3 → 2 → 1. Holding Home five seconds remains a direct return from any app.

`scripts/workspace-action` queries live Hyprland windows and changes only workspace
focus. It does not issue browser navigation, restart the application, or reopen
its library. Jellyfin remains on workspace 2; Moonlight is reserved workspace 3.
The reviewed catalog supplies each application's window class.

## Isolating Jellyfin input

MPV's SDL gamepad input is separate from compositor keyboard focus. Reading the
same controller in the shell alone does not prevent background library navigation.
The Act I profile now loads `adapters/mpv/act_i_input_guard.lua` as a separate MPV
script. It blocks native gamepad keys while the window is unfocused, while Home
is reserved, and until held controls have been released after a transition.
When unblocked, it removes its overlays, leaving Jellyfin's own A/B and other
bindings in place. Guide (`GAMEPAD_MENU` in MPV) is reserved for Act I.

The input reader delivers physical Home/release state to the guard through the
profile's private local MPV IPC socket. This is independent of the launch helper,
so switching directly to a workspace or restarting Home does not lose routing.
MPV's logical key cancellation is not mistaken for a physical Home release.
No keyboard injection, exclusive controller grab, root input service or additional
system-device permissions are introduced.

The adapter installs only the managed Lua file and its IPC option. Existing
Jellyfin JSON settings and credentials are preserved; a pre-existing different
MPV IPC server is reported instead of replaced. Existing clients need one restart
to load the script. Normal workspace transitions do not restart them.

## Hardware acceptance

With the KK3 Max in Switch mode and Jellyfin MPV Shim 3.3.0, the owner verified:

- Open a film detail page, hold Home five seconds, navigate Act I Home, then
  select Jellyfin again: the same detail page remains open.
- Repeat the Home return, then use Home + D-pad right: the same page remains.
- Film-page preservation and native input after shortcut re-entry were verified.
  The updated cycle includes Home. Live compositor command checks confirmed
  1 → 2 → 1 in both directions with the same Jellyfin process; the updated
  gamepad toggle still needs owner-observed acceptance.
- D-pad and the existing Jellyfin B-select/A-back controls work after re-entry.

The Jellyfin window retained the same process throughout those transitions. Live
MPV IPC confirmed the guard was loaded and normal face-button bindings remained
native while focused. Automated tests cover multi-app ordering, closed-app
skipping, one-shot chords, canceled long holds and guard release behavior.

Only Jellyfin is installed for the current hardware tests. Two-application cycling
and input isolation for Moonlight still require its own adapter and acceptance
when Sunshine is available. Playback pause/audio and display-mode policy are
separate future work; these shortcuts currently change workspace focus only.
