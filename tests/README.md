# Validation

Run on the dedicated target:

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
QT_QPA_PLATFORM=offscreen /usr/lib/qt6/bin/qmltestrunner -input tests -o -,txt
```

Python checks cover Nintendo/standard button positions, edge-triggered selection,
dead zones, repeat timing, focus loss/re-entry and the five-second Home threshold.
Qt Quick tests cover keyboard and gamepad actions through the same Home component.
Neither suite proves physical device access, Bluetooth reconnection, application
routing, audio, HDR or display switching. See the manual hardware acceptance steps
in [gamepad input](../docs/gamepad.md) and [session usage](../docs/manual-session.md).
