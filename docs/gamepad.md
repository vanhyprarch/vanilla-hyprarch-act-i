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
newline-delimited JSON over standard input/output. It discovers only udev
`ID_INPUT_JOYSTICK=1` event devices, monitors hotplug and uses the active local
session's device ACLs. It never grabs the device or injects keyboard events.
Do not add the HTPC account to the broad `input` group or run the reader as root.

The Qt window's active state gates ordinary Home input in both the reader and
the shell. Losing focus cancels directional repeat. Held controls cannot repeat
into Home on re-entry. D-pad and left stick repeat after 400 ms, then every 160 ms;
stick input uses a 35 percent dead zone. A/B activate once per press.

Holding Home (`BTN_MODE`) for five seconds requests workspace 1 once, including
when an application has focus. Release it before the shortcut can fire again.
Short presses do not change workspace. Input remains visible to the application:
the start of a long press can also reach Moonlight and the remote PC. Moonlight
behavior remains a hardware acceptance task when Sunshine is available. The
L+R+Start+Select Moonlight disconnect chord is not assigned by Act I.

The reader exits when the shell closes its input pipe. Disconnecting a controller
removes its repeat/hold state; udev device creation triggers discovery on reconnect.
Reader failure leaves keyboard recovery available. A global Home shortcut needs
its own physical acceptance check; software timing tests do not prove it on a TV.

## Checks

Run on the dedicated target:

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
QT_QPA_PLATFORM=offscreen /usr/lib/qt6/bin/qmltestrunner -input tests -o -,txt
```

Then verify navigation, modal back, held Home from another workspace, disconnect
and reconnect, and that ordinary input goes to the focused application. These
checks do not validate application playback, game streaming, HDR or refresh rates.
