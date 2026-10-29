# Workspace navigation and preserved application state

| Control | Behavior |
| --- | --- |
| Hold Home and click D-pad left | Focus the previous workspace (Home or an open app) |
| Hold Home and click D-pad right | Focus the next workspace (Home or an open app) |
| Select an application tile | Focus its existing window, or launch it if closed |

Keep Home pressed for as many workspace changes as needed. Each new D-pad click
produces one step; release the direction between clicks, or change direction.
Holding a direction does not auto-repeat workspace switching. Stick movement
does not trigger shortcuts. Home by itself has no action, regardless of duration;
there is no timed return-to-Home shortcut. Super+H remains keyboard recovery.

Release Home to return to normal application controls. The Jellyfin guard keeps
held transition inputs blocked until controls are released. Rapid workspace
requests are executed in order rather than discarded while a previous change
is in progress. The controller-only Home navigation mapping is unchanged.

Home always participates in the cycle as workspace 1. Open applications follow
in workspace order. Closed or unmapped applications are skipped without being
launched; with none open, either direction stays on Home.

With only Jellyfin open, both directions toggle Home (1) and Jellyfin (2).
With Jellyfin and Moonlight open, right cycles 1 → 2 → 3 → 1, while left cycles
1 → 3 → 2 → 1.

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

- Keep Home pressed and click left/right repeatedly: each click changes between
  Act I Home and Jellyfin without releasing Home.
- The same film detail page remains open on re-entry.
- Hold Home alone for at least six seconds: no workspace change occurs.
- Release all controls: D-pad and the existing Jellyfin B-select/A-back mappings
  work normally again.

Earlier live compositor checks verified 1 → 2 → 1 in both directions with the same
Jellyfin process. Live MPV IPC confirmed that the guard loads and native
face-button bindings remain in place while focused. Automated tests cover
multi-app order, closed-app skipping, repeated clicks across focus changes,
absence of timed Home actions, held-direction suppression and guard release.

Only Jellyfin is installed for the current hardware tests. Two-application cycling
and input isolation for Moonlight still require its own adapter and acceptance
when Sunshine is available. These shortcuts change workspace focus only; the
separate Jellyfin playback policy pauses a film on focus loss and leaves manual
resume to the user. See [media acceptance](media-playback.md). Broader audio and
display-mode policy remain future work.
