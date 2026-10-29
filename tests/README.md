# Validation

Run on the dedicated target:

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
lua tests/test_input_guard.lua
lua tests/test_playback_policy.lua
QT_QPA_PLATFORM=offscreen /usr/lib/qt6/bin/qmltestrunner -input tests -o -,txt
```

Python checks cover Nintendo/standard button positions, edge-triggered selection,
dead zones, repeat timing, focus loss/re-entry, repeated clicks during one Home
hold, suppression of held-direction shortcuts and absence of timed Home actions.
Qt Quick tests cover keyboard and gamepad actions through the same Home component.
Neither suite proves physical device access, Bluetooth reconnection, application
routing, audio, HDR or display switching. See the manual hardware acceptance steps
in [gamepad input](../docs/gamepad.md) and [session usage](../docs/manual-session.md).

Workspace tests cover live-app ordering and skipping closed/unmapped windows.
The Lua harness checks guard focus, native face-button preservation, reserved
Guide, logical key cancellation, and release quarantine. Hardware checks confirm
film-page preservation, left/right shortcuts with one app, and input after return;
multi-app Moonlight acceptance remains pending.

The playback-policy Lua harness checks automatic pause on video focus loss,
manual-only resume, already-paused content and idle/audio/image exclusions.
