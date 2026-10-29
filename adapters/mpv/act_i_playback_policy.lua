-- SPDX-License-Identifier: GPL-2.0-only
-- Pause real video when leaving its window; never resume without user input.
local marker = "user-data/act-i/playback-policy-loaded"
if mp.get_property_native(marker, false) then return end
local focused = mp.get_property_native("focused", false) == true

local function pause_background_video()
    if focused or mp.get_property_native("idle-active", true)
       or mp.get_property_native("pause", false) then return end
    for _, track in ipairs(mp.get_property_native("track-list", {})) do
        if track.type == "video" and track.selected and not track.albumart
           and not track.image then
            mp.set_property_native("pause", true)
            return
        end
    end
end

mp.observe_property("focused", "bool", function(_, value)
    if value == nil then return end
    focused = value == true
    pause_background_video()
end)
mp.register_event("file-loaded", pause_background_video)
mp.set_property_native(marker, true)
