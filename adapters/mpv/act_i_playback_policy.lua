-- SPDX-License-Identifier: GPL-2.0-only
-- Pause real video only on workspace exit; never resume without user input.
local marker = "user-data/act-i/playback-policy-loaded"
if mp.get_property_native(marker, false) then return end
local workspace_active = true

local function pause_background_video()
    if workspace_active or mp.get_property_native("idle-active", true)
       or mp.get_property_native("pause", false) then return end
    for _, track in ipairs(mp.get_property_native("track-list", {})) do
        if track.type == "video" and track.selected and not track.albumart
           and not track.image then
            mp.set_property_native("pause", true)
            return
        end
    end
end

-- Window activation can transiently disappear while MPV changes video output.
-- The session manager supplies compositor workspace state instead of treating
-- that transient focus loss as leaving Jellyfin.
mp.register_script_message("act-i-workspace", function(value)
    workspace_active = value == "yes"
    pause_background_video()
end)
mp.register_event("file-loaded", pause_background_video)
mp.set_property_native(marker, true)
