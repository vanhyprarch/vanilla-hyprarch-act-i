# Display baseline

Observed on T8 on 2026-10-29 using libdisplay-info 0.3.0-1:

```sh
di-edid-decode /sys/class/drm/card1-HDMI-A-2/edid
```

## Receiver-advertised capabilities

Connected receiver: LG TV SSCR2. The 256-byte EDID advertises:

| Feature | Advertised value |
| --- | --- |
| Preferred detailed timing | 3840x2160 at 60 Hz |
| UHD video timings | 3840x2160 at 24, 25, 30, 50, 60, 100 and 120 Hz |
| QHD detailed timing | 2560x1440 at approximately 119.998 Hz |
| Full HD progressive timings | 1920x1080 at 24, 25, 30, 50, 60, 100 and 120 Hz |
| HDR transfer functions | SMPTE ST 2084 (PQ) and Hybrid Log-Gamma (HLG) |
| HDR static metadata | Type 1 |
| Colorimetry | BT.2020 RGB and YCC |
| HDMI Forum maximum TMDS character rate | 600 MHz |
| HDMI Forum FRL | Advertised up to 12 Gbps per lane on four lanes |
| Variable refresh range | 40-120 Hz |
| Other receiver features | ALLM, QMS and DSC advertised |

The EDID also contains a Dolby vendor block. This is not evidence of a working
Dolby Vision pipeline and does not add Dolby Vision to the initial project scope.

The decoder prints nominal integer-rate CTA video timings. Availability of
23.976/29.97/59.94 Hz and other fractional variants still needs kernel/compositor
mode enumeration; do not infer verified fractional support from this table.

## Conformance warning

The decoder returned exit status 254 and reported:

```text
Vendor-Specific Data Block (HDMI Forum), OUI C4-5D-D8:
Bits 4 and 5 of byte 11 are reserved.
EDID conformity: FAIL
```

Decoding produced readable capabilities, but this warning must remain visible in
test records. Do not alter or override the EDID based on this warning alone.

## What remains unverified

These are receiver advertisements, not confirmed modes of the complete T8 GPU,
port, cable, driver and compositor path. No mode change was requested during this
inspection. In particular, 4K120, HDR output, deep color, VRR and fractional-rate
switching remain untested.

Next: establish a stable SDR graphical baseline, inspect compositor/driver modes,
and then validate display-reported output and playback statistics. Keep the
preferred resolution fixed unless the owner opts into resolution switching.
