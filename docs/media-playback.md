# Jellyfin media playback acceptance

Status: M3 is in progress. The first 1080p-class SDR file has passed hardware
decoding, visible-image/audio, controller pause/resume, SRT rendering and seek
recovery checks. This is not
4K, HDR, automatic refresh matching or full-format acceptance.

## Configure through the client

Use Jellyfin MPV Shim's own **Settings → Playback → Hardware Decoding → On**.
Stop playback, save the preference, close/reopen the client and play the same
file for comparison. The saved value is `auto`; inspect MPV's `hwdec-current`
to verify the decoder actually selected. A requested option alone is not proof.

Use a fresh client startup for acceptance. Switching decoder modes inside an
already-playing software session caused a video-output initialization failure
in this build. Recovery used the client's saved preference after a fresh startup.
Runtime decoder switching is not validated by this acceptance record.

Existing user preferences remain outside Git. No global hardware-decoding
preference is forced on other GPUs by this acceptance record.

## Source-based color signalling

The managed MPV profile uses `target-colorspace-hint-mode=source`. With current
MPV builds, the default `target` mode can describe an HDR-capable display and
convert SDR into an HDR output. Source mode describes the content instead, as
required by [Hyprland auto-HDR](https://wiki.hypr.land/Configuring/Basics/Variables/).
See also the [MPV color hint documentation](https://mpv.io/manual/stable/#options-target-colorspace-hint-mode).
An existing conflicting setting is reported for review rather than overwritten.
This setting does not force HDR or change decoder or controller preferences.

An isolated fresh-client test at 1920x1080/60 with an SDR BT.709 source passed
autostart and keyboard pause/resume after this change. No DRM hotplug or monitor
removal events occurred during the observed test. Integrated launcher/gamepad
startup also passed with the output restored to
3840x2160/60: the owner confirmed continuous picture/audio, no HDR notification,
and working player pause/resume. A live sample confirmed focus, VA-API, source
and render-target BT.709/BT.1886, and zero decoder/output drops. This used the
same 1080p-class source; it does not validate 4K media or HDR playback. A
subsequent cold-launch check passed graceful close, automatic Home return,
reopen without authentication, autostart and controller pause/resume. Its complete
startup observation showed no DRM hotplug or monitor disappearance.

## Wayland graphics compatibility

The tested Vulkan/Wayland path intermittently stalled for about eight seconds
when starting, seeking or returning to the library. Native video-output thread
snapshots taken one and three seconds after Play both showed
`drmSyncobjTimelineWait` through `wsi_drm_wait_for_explicit_sync_release` and
`wsi_wl_swapchain_acquire_next_image_explicit`. Player API queries could also
stall. This locates the observed wait in the explicit-sync image-release path;
it does not establish which upstream component introduced it. Early file-load
or playback events alone did not prove prompt visible playback.

A per-user compatibility profile avoided that Vulkan path:

```ini
gpu-api=opengl
gpu-context=wayland
```

Add these only with the client fully closed, after backing up its private
`mpv.conf` under the Flatpak configuration directory. Preserve the managed app
ID, IPC option and source-based color hint. These options select the rendering
API/context; the client's hardware-decoding preference remains independent.
The adapter preserves these existing options on subsequent launches.

With the current `gpu-next` renderer using OpenGL/Wayland, the owner verified
three consecutive rapid Play/start and keyboard-Q/stop cycles. All three native
logs confirmed `vaapi` decoding and VA-API/NV12 video output, with no errors.
A subsequent forward seek and Home/app workspace round trip also passed: the
film remained paused with silent audio on return. The final sample confirmed
native Wayland focus, `vaapi`, SDR BT.709/BT.1886 input and render target, and
zero decoder/output frame drops with the display at 3840x2160/60.

This is a target-tested compatibility choice, not a forced renderer default for
all GPUs. The source was 1080p-class H.264 SDR; 4K media and HDR output through
this rendering path still require hardware acceptance. Detailed traces and
screenshots remain private and outside Git.

## Verified SDR sample

| Measurement | Result |
| --- | --- |
| Source video | H.264, 1920×1036 (1080p class), 23.976025 fps |
| Source color | BT.709 / BT.1886, SDR |
| Requested decoder | `auto`, selected in the client menu |
| Active decoder and interop | `vaapi` / `vaapi` |
| Hardware surfaces | VA-API with underlying NV12, without a copy-back path |
| Decoder drops / output drops / delayed frames | All zero at both samples, 12 seconds apart |
| MPV A/V difference | Approximately 0.00002 seconds at the samples |
| Display during the test | 3840×2160 at 60 Hz, SDR |
| Audio | Owner confirmed output through the LG TV over HDMI |

The owner confirmed normal image, no apparent corruption/flicker/color issues,
and synchronized speech. MPV's small sampled A/V difference supports that check;
it is not a measurement of end-to-end TV latency.

The owner also paused and resumed through the controller. MPV reported pause
then resume with the same playback position, and `vaapi` remained active.

The 23.976 fps source is still displayed at 60 Hz. Zero dropped frames does not
prove correct film cadence; automatic refresh matching belongs to M4.

The owner enabled and saw an internal SubRip (SRT) subtitle track. MPV reported
subtitle visibility on, zero subtitle delay, VA-API still active and zero frame
loss counters. Other subtitle formats are not covered by this sample.

The owner performed a forward seek. The subsequent sample confirmed active
video/VA-API, selected visible subtitles, zero frame loss counters and near-zero
MPV A/V difference. The precise jump distance was not measured.

## Remaining checks

- Other subtitle formats and broader subtitle synchronization acceptance.
- 4K SDR and additional codecs, then HDR → SDR behavior on the real TV.
- Refresh matching and display-mode restoration in M4.
- Audio channel mapping and passthrough remain separate investigations.

Detailed samples and private application logs stay outside the repository.
Do not commit server addresses, media paths, authentication or personal titles.

## Leaving Jellyfin during a film

Act I's session monitor reports the active Hyprland workspace to
`act_i_playback_policy.lua`. A real selected video track pauses when leaving
Jellyfin's workspace for Home or another app workspace. Returning never resumes
playback automatically; the user chooses Resume. An already-paused film remains paused. Video loaded while the
Jellyfin workspace is already in the background is also paused on the
file-loaded event.

Idle library backgrounds, still images, album art and audio-only playback are
excluded. Their broader background-audio policy remains separate work. The
behavior is specific to the initial single-output HTPC session; it is not a
claim about multi-monitor focus or remote Moonlight game pausing.

The adapter installs this managed MPV script alongside the input guard, without
changing the client's saved decoder preference or face-button mappings. Unit
checks cover workspace departure, no automatic resume, already-paused content
and the idle/audio/image exclusions.

The owner physically verified pause on switching to Home, continued pause with
silent audio after returning, and a correct manual resume. MPV confirmed a fixed
playback position during the paused return and VA-API still active after resume.
The same client stayed open; no reload or decoder preference change was required.

## Workspace monitor recovery

The session monitor reconnects and resamples the active workspace after a
transient compositor query failure or event-stream closure, reporting the error
instead of silently abandoning playback policy. It reports workspace state
before attempting optional window-focus repair.

After restarting the Home-owned bridge, the owner repeated manual resume,
workspace exit, and return. The event trace confirmed pause on workspace exit,
continued pause after focus returned, and no automatic unpause. The owner
confirmed silent audio, while VA-API and native controller input remained active.
