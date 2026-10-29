# Configuration

- `hypr/hyprland.lua`: isolated Act I session configuration, selected explicitly
  by `scripts/start-session` without replacing the user's normal Hyprland config.
- `apps.json`: reviewed application names, Flatpak IDs and workspace assignments.
- `greetd/config.toml.in`: automatic-start template with placeholders;
  activation and boot validation require owner authorization.

Keep personal overrides in ignored `config/local/` files. Never commit rendered
machine-specific login configuration, credentials or maintenance logs.
