-- SPDX-License-Identifier: GPL-2.0-only
-- Dedicated Act I session. Hyprland 0.57 or newer; no default user config is replaced.
local repo = assert(os.getenv("ACT_I_REPO_DIR"), "Start using scripts/start-session")
local function quote(value)
    return "'" .. value:gsub("'", "'\\''") .. "'"
end
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto", cm = "srgb", bitdepth = 8 })
hl.config({
    general = { gaps_in = 0, gaps_out = 0, border_size = 0 },
    decoration = { rounding = 0, blur = { enabled = false }, shadow = { enabled = false } },
    animations = { enabled = false },
    input = { kb_layout = os.getenv("ACT_I_KEYBOARD_LAYOUT") or "us", follow_mouse = 0 },
})
hl.window_rule({
    name = "act-i-jellyfin",
    match = { class = "^org\\.vanhyprarch\\.acti\\.jellyfin$" },
    workspace = "2",
    fullscreen_state = "2 0",
    suppress_event = "fullscreen",
})
hl.bind("SUPER + SHIFT + E", hl.dsp.exit())
hl.bind("SUPER + H", hl.dsp.focus({ workspace = 1 }))
hl.bind("SUPER + R", hl.dsp.exec_cmd(quote(repo .. "/scripts/start-home")))
hl.on("hyprland.start", function()
    hl.exec_cmd(quote(repo .. "/scripts/start-home"))
end)
