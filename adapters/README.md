# Application adapters

`catalog.py` loads the reviewed Flatpak catalog. `jellyfin.py` supplies the first
application adapter: a stable Wayland window class and a profile initializer that
preserves existing settings and credentials. An adapter exposes `WINDOW_CLASS`
and `prepare_profile(flatpak_id)` to the shared application session helper.

Playback metadata, HDR/refresh requests and the Moonlight adapter remain later
increments. Keep their app-specific details outside shared session/display policy.
