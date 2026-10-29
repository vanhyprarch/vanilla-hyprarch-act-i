# Home gamepad input

The first hardware-verified controller is the GuliKit KK3 Max in Nintendo Switch
mode over Bluetooth. The owner confirmed D-pad and left-stick selection, physical
A for selection and physical B for back on the TV. Xbox and PlayStation physical
acceptance remains pending; the standard mapping uses south to select, east back.

## Implementation

Install the official Arch packages `python-evdev` and `python-pyudev`. Bluetooth
controllers additionally require the normal BlueZ stack and an enabled adapter.
Pair and trust the intended controller through BlueZ outside the repository;
never commit adapter addresses, controller addresses or pairing data.

Quickshell owns `scripts/gamepad-events`, an unprivileged Python child with
newline-delimited JSON over standard input/output. A bounded asynchronous routing
worker sends physical Home/release state to the Jellyfin MPV guard through its
private IPC socket, independently of Quickshell's launch-helper lifecycle. It discovers only udev
`ID_INPUT_JOYSTICK=1` event devices, monitors hotplug and uses the active local
session's device ACLs. It never grabs the device or injects keyboard events.
Do not add the HTPC account to the broad `input` group or run the reader as root.

The Qt window's active state gates ordinary Home input in both the reader and
the shell. Losing focus cancels directional repeat. Held controls cannot repeat
into Home on re-entry. D-pad and left stick repeat after 400 ms, then every 160 ms;
stick input uses a 35 percent dead zone. A/B activate once per press.

Holding Home (`BTN_MODE`) for five seconds requests workspace 1 once, including
when an application has focus. Release it before the shortcut can fire again.
Home + D-pad left/right cycles Home and already-open application workspaces once per Home
press and cancels the long-hold timer. Jellyfin now has an MPV input guard that
reserves Guide and blocks background/held-transition input, preserving its native
face-button bindings. See [workspace navigation](workspace-navigation.md).
Moonlight input isolation and forwarding remain separate acceptance work when
Sunshine is available. The
L+R+Start+Select Moonlight disconnect chord is not assigned by Act I.

The reader exits when the shell closes its input pipe. Disconnecting a controller
removes its repeat/hold state; udev device creation triggers discovery on reconnect.
Reader failure leaves keyboard recovery available. The owner physically verified
that the five-second Home hold returns from the Jellyfin library to Act I.
Moonlight behavior and Bluetooth reconnect still need their own acceptance checks.

## Checks

Run on the dedicated target:

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
QT_QPA_PLATFORM=offscreen /usr/lib/qt6/bin/qmltestrunner -input tests -o -,txt
```

Navigation, modal back, held Home from Jellyfin and tile-based re-entry have passed
physical checks. Continue with disconnect/reconnect and ordinary input routing
for each newly supported application. These
checks do not validate application playback, game streaming, HDR or refresh rates.

## Face-button convention

The current Home uses physical Nintendo A (east) to select and B (south) for back.
The owner observed the opposite, positional convention in Jellyfin: B (south)
selects and A (east) goes back. Preserve both current mappings until the owner
chooses a unified Act I convention. Do not infer physical button behavior solely
from an SDL label or a Jellyfin setting name.
