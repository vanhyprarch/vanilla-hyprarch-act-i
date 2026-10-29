# Application adapters

`catalog.py` loads the reviewed Flatpak catalog. `jellyfin.py` supplies the first
application adapter: a stable Wayland window class and a profile initializer that
preserves existing Jellyfin JSON settings and credentials. The managed
`mpv/act_i_input_guard.lua` and private MPV IPC option isolate background input
and reserve Act I's Home combinations without remapping native A/B controls. An adapter exposes `WINDOW_CLASS`
and `prepare_profile(flatpak_id)` to the shared application session helper.

Playback metadata, HDR/refresh requests and the Moonlight adapter remain later
increments. Keep their app-specific details outside shared session/display policy.
