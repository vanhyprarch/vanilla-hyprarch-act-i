-- SPDX-License-Identifier: GPL-2.0-only
local properties = {focused=true, ["idle-active"]=false, pause=false,
    ["track-list"]={{type="video", selected=true, albumart=false, image=false}}}
local observers, events, messages = {}, {}, {}
local pauses = 0
mp = {
    get_property_native=function(key, fallback)
        if properties[key] == nil then return fallback end
        return properties[key]
    end,
    set_property_native=function(key,value)
        properties[key]=value
        if key=="pause" then pauses=pauses+1 end
    end,
    observe_property=function(name, _, callback) observers[name]=callback end,
    register_event=function(name, callback) events[name]=callback end,
    register_script_message=function(name, callback) messages[name]=callback end,
}
dofile("adapters/mpv/act_i_playback_policy.lua")
messages["act-i-workspace"]("yes")
assert(not properties.pause and pauses==0, "Focused playback is unchanged")
messages["act-i-workspace"]("no")
assert(properties.pause and pauses==1, "Leaving a video pauses once")
messages["act-i-workspace"]("yes")
assert(properties.pause and pauses==1, "Returning never auto-resumes")
messages["act-i-workspace"]("no")
assert(pauses==1, "Already-paused content is preserved")
properties.pause=false
properties["idle-active"]=true
events["file-loaded"]()
assert(not properties.pause, "Idle library is not paused")
properties["idle-active"]=false
properties["track-list"]={{type="audio",selected=true}}
events["file-loaded"]()
assert(not properties.pause, "Audio-only playback is not part of video policy")
properties["track-list"]={{type="video",selected=true,albumart=true}}
events["file-loaded"]()
assert(not properties.pause, "Album art is not a movie")
properties["track-list"]={{type="video",selected=true,image=true}}
events["file-loaded"]()
assert(not properties.pause, "Still-image library backgrounds are excluded")
properties["track-list"]={{type="video",selected=true}}
events["file-loaded"]()
assert(properties.pause and pauses==2, "Video loaded in background starts paused")
assert(observers.focused==nil, "Transient window focus does not pause video")
local original=messages["act-i-workspace"]
dofile("adapters/mpv/act_i_playback_policy.lua")
assert(messages["act-i-workspace"]==original, "Duplicate activation does not add observers")
print("PASS: video workspace-exit pause, manual-only resume, idle/audio/image exclusions")
