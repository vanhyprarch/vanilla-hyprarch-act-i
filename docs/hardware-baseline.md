# T8 hardware baseline

Observed: 2026-10-29. This document describes the dedicated development and test
machine, not the production workstation. T8 is its operational name; no hostname
change was performed. Personal addresses, machine IDs and device serial numbers
are deliberately omitted.

## Verified by read-only inspection

| Item | Observation |
| --- | --- |
| OS | Arch Linux, x86_64 |
| Running kernel | 7.2.11-arch1-1 |
| CPU | Intel N100, four cores/four threads |
| RAM | Approximately 16 GB installed; `free` reports 15 GiB |
| GPU | Intel Alder Lake-N UHD Graphics, PCI ID 8086:46d1 |
| Active graphics driver | i915 |
| Storage | 512 GB SATA SSD; approximately 477 GiB exposed |
| Filesystem | Btrfs for root and home; separate FAT boot partition |
| Free home-filesystem space | Approximately 473 GiB at baseline |
| Swap | 4 GiB zram |
| Network | One active wired Gigabit Ethernet interface |
| Display | LG TV on HDMI-A-2; connector connected and enabled |
| Resolution enumeration | Includes 3840x2160, 2560x1440 and 1920x1080 |
| EDID | 256 bytes exposed by the connected output |
| Audio hardware | Intel HDA HDMI outputs and USB audio device |
| Input | Logitech K400 Plus and additional wireless HID receiver |
| Gamepad | None observed in the current kernel input inventory |
| Bluetooth hardware | Realtek and TP-Link USB adapters enumerated; operation untested |

The HDMI ELD reports LPCM stereo and AC-3, E-AC-3, DTS, DTS-HD and MLP/TrueHD
capabilities. These are receiver-advertised capabilities, not successful playback
or passthrough test results. PipeWire and WirePlumber are not installed yet.

## Access and software baseline

- Non-root, key-based SSH commands work directly from Codex.
- The server host-key fingerprint was checked against the physical console.
- Remote temporary-file creation, overwrite and read succeeded; the probe was removed.
- OpenSSH is enabled and active; version observed: 10.6p1-2.
- Sudo is installed and the development user belongs to wheel. A non-interactive
  policy query required a password; administrative access is not proven by group
  membership alone.
- Git, Hyprland, Quickshell, MPV, Jellyfin MPV Shim, Moonlight, PipeWire and
  WirePlumber were absent at the initial inspection.
- Base system includes NetworkManager, Intel microcode, Limine, Snapper and zram.

## Pending validation

1. Decode EDID: advertised timings, fractional rates, HDR metadata and link limits.
2. Compare advertised modes with modes accepted by the driver and compositor.
3. Establish a stable SDR baseline before HDR and automatic mode switching.
4. Validate hardware video decoding, HDMI audio and any passthrough configuration.
5. Connect the selected Xbox/PlayStation controller and verify routing.

The owner reports a modern 4K/HDR/120 Hz LG TV. Neither 4K120 output nor HDR
operation has been verified on the current PC, cable, port and software stack.

## M0 follow-up: approved tooling and repository

On 2026-10-29, password-protected sudo successfully installed `git 2.56.0-1`
and `libdisplay-info 0.3.0-1`, with their required dependencies. No full system
upgrade, graphical package installation, reboot or display-mode change occurred.

Git was initialized on T8 in the approved remote directory using branch `main`.
The owner confirmed commit author details; GitHub authentication remains pending. See the
[display baseline](display-baseline.md) for the decoded EDID and its conformance
warning. The production workstation contains no project checkout created by this
workflow.
