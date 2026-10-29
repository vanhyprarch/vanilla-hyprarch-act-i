# SPDX-License-Identifier: GPL-2.0-only
"""Jellyfin profile setup; existing preferences and credentials are preserved."""
import json
from pathlib import Path

WINDOW_CLASS = "org.vanhyprarch.acti.jellyfin"
DEFAULTS = {
    "fullscreen": True,
    "browser_fullscreen": True,
    "input_gamepad": True,
    "close_to_tray": False,
    "allow_background": False,
    "mpv_idle_quit": False,
}


def prepare_profile(flatpak_id, home=None):
    home = Path.home() if home is None else Path(home)
    folder = home / ".var/app" / flatpak_id / "config/jellyfin-mpv-shim"
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    conf = folder / "conf.json"
    if not conf.exists():
        with conf.open("x") as stream:
            stream.write(json.dumps(DEFAULTS, indent=2) + "\n")
        conf.chmod(0o600)
    mpv = folder / "mpv.conf"
    if not mpv.exists():
        with mpv.open("x") as stream:
            stream.write(f"wayland-app-id={WINDOW_CLASS}\n")
        mpv.chmod(0o600)
    # Never replace an existing MPV profile or silently take over another app ID.
    values = [line.split("=", 1)[1].strip() for line in mpv.read_text().splitlines()
              if line.strip().startswith("wayland-app-id=")]
    if not values or values[-1] != WINDOW_CLASS:
        raise ValueError("Jellyfin mpv.conf needs wayland-app-id=" + WINDOW_CLASS)
    return folder
