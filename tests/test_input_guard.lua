-- SPDX-License-Identifier: GPL-2.0-only
local bindings, observers, messages, properties = {}, {}, {}, {}
mp = {
    add_forced_key_binding = function(key, name, callback) bindings[name] = callback end,
    remove_key_binding = function(name) bindings[name] = nil end,
    observe_property = function(name, _, callback) observers[name] = callback end,
    register_script_message = function(name, callback) messages[name] = callback end,
    set_property_native = function(name, value) properties[name] = value end,
}
dofile("adapters/mpv/act_i_input_guard.lua")
local function blocked() return properties["user-data/act-i/input-blocked"] end
local function route(home, neutral) messages["act-i-routing"](home, neutral) end
assert(blocked(), "Startup is blocked until focus is known")
observers.focused("focused", true)
route("no", "yes")
assert(not blocked(), "Focused neutral gamepad retains native controls")
assert(bindings.act_i_ACTION_DOWN == nil, "Native face-button binding is not replaced")
observers.focused("focused", false)
assert(blocked(), "Background gamepad input must be blocked")
route("no", "no")
observers.focused("focused", true)
assert(blocked(), "Home selection held across re-entry must not reach Jellyfin")
route("no", "yes")
assert(not blocked(), "Release re-arms native gamepad input")
bindings.act_i_home({event="down"})
assert(blocked(), "Guide is reserved immediately before IPC updates")
bindings.act_i_home({event="up", canceled=true})
assert(blocked(), "Logical MPV cancellation is not a physical Guide release")
route("yes", "no")
route("no", "no")
assert(blocked(), "Held chord direction must not leak on Guide release")
route("no", "yes")
assert(not blocked(), "A fully released chord restores native bindings")
assert(bindings.act_i_home ~= nil, "Guide remains reserved even while other keys pass")
print("PASS: MPV focus, native A/B preservation, Guide reservation and release quarantine")
