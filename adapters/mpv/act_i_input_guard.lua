-- SPDX-License-Identifier: GPL-2.0-only
-- Gate SDL input without changing Jellyfin's native face-button bindings.
local keys = {
    "ACTION_DOWN", "ACTION_RIGHT", "ACTION_LEFT", "ACTION_UP", "BACK", "START",
    "LEFT_STICK", "RIGHT_STICK", "LEFT_SHOULDER", "RIGHT_SHOULDER",
    "DPAD_UP", "DPAD_DOWN", "DPAD_LEFT", "DPAD_RIGHT",
    "LEFT_STICK_UP", "LEFT_STICK_DOWN", "LEFT_STICK_LEFT", "LEFT_STICK_RIGHT",
    "RIGHT_STICK_UP", "RIGHT_STICK_DOWN", "RIGHT_STICK_LEFT", "RIGHT_STICK_RIGHT",
    "LEFT_TRIGGER", "RIGHT_TRIGGER",
}
local focused = false
local reserved = false
local neutral = true
local quarantine = true
local blocked = nil

local function update()
    local wanted = not focused or reserved or quarantine
    if wanted == blocked then return end
    blocked = wanted
    for _, key in ipairs(keys) do
        local name = "act_i_" .. key
        if wanted then
            mp.add_forced_key_binding("GAMEPAD_" .. key, name, function() end,
                                     {complex = true})
        else
            mp.remove_key_binding(name)
        end
    end
    mp.set_property_native("user-data/act-i/input-blocked", wanted)
end

-- MPV calls SDL's Guide button GAMEPAD_MENU. Never deliver it to the client.
mp.add_forced_key_binding("GAMEPAD_MENU", "act_i_home", function(event)
    if event.event == "down" or event.event == "press" then
        reserved = true
        quarantine = true
        update()
    end
    -- Physical release comes from Act I: MPV can logically cancel this key
    -- when another key is pressed, which is not a real Home-button release.
end, {complex = true})

mp.observe_property("focused", "bool", function(_, value)
    focused = value == true
    quarantine = not neutral
    update()
end)

mp.register_script_message("act-i-routing", function(home, released)
    local was_reserved = reserved
    reserved = home == "yes"
    neutral = released == "yes"
    if reserved or (was_reserved and not neutral) then quarantine = true end
    if neutral and not reserved then quarantine = false end
    update()
end)

update()
