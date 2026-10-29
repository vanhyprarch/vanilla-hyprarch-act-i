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

Act I's `act_i_playback_policy.lua` observes the MPV window's focus. A real selected
video track pauses when the window loses focus, including switching to Home or
another app workspace. Returning never resumes playback automatically; the user
chooses Resume. An already-paused film remains paused. Video loaded while the
window is already in the background is also paused on the file-loaded event.

Idle library backgrounds, still images, album art and audio-only playback are
excluded. Their broader background-audio policy remains separate work. The
behavior is specific to the initial single-output HTPC session; it is not a
claim about multi-monitor focus or remote Moonlight game pausing.

The adapter installs this managed MPV script alongside the input guard, without
changing the client's saved decoder preference or face-button mappings. Unit
checks cover focus loss, no automatic resume, already-paused content and the
idle/audio/image exclusions.

The owner physically verified pause on switching to Home, continued pause with
silent audio after returning, and a correct manual resume. MPV confirmed a fixed
playback position during the paused return and VA-API still active after resume.
The same client stayed open; no reload or decoder preference change was required.
