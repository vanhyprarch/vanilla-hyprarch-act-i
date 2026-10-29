# Remote-only development workflow

## Authoritative location

The only project checkout is on T8 at:

```text
~/Projects/vanilla-hyprarch-act-i
```

The production workstation is an SSH client. Do not clone, mirror, build or test
the project there. Send edits over SSH stdin or use an explicitly remote editor.
All Git commands, commits, builds and runtime tests execute on T8.

Before project operations, verify the remote identity and working directory.
After Git initialization, confirm the repository with:

```sh
cd ~/Projects/vanilla-hyprarch-act-i
pwd
git rev-parse --show-toplevel
git status --short --branch
```

## SSH and privilege handling

Use the dedicated non-root SSH identity and strict host-key verification. Keep
private keys and passphrases out of the repository and documentation. The SSH
agent unlock is temporary; an expired key must be unlocked by its owner again.
Do not persist a workstation-specific socket path in project configuration.

Keep sudo password protected. Do not enable broad passwordless sudo, unrestricted
root SSH, or disable host-key checking. Apply only authorized system changes.
A functioning graphical console remains the recovery path during setup.

## Git and publication

The owner selected GitHub account `vanhyprarch`. The intended new project slug is
`vanilla-hyprarch-act-i`; verify availability and account authorization before
creating or connecting it. Existing projects are independent and must not be
modified. The owner confirmed public visibility and the commit identity
`vanhyprarch <vanhyprarch@proton.me>`.

Use GPL-2.0-only and English for repository content and commit messages. Never
invent an author email or publish an unconfirmed personal address. Commit reviewed
changes on T8 before significant system changes once Git is available.

The T8 disk alone is not a backup. A separately authorized GitHub remote will
provide off-machine source storage; keep credentials and private hardware/network
identifiers out of published files.
