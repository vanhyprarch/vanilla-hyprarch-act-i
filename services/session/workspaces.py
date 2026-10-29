# SPDX-License-Identifier: GPL-2.0-only
"""Workspace navigation never launches an application or sends it UI commands."""


def target_workspace(action, applications, clients, current):
    if action == 'home':
        return 1
    open_workspaces = sorted({app.workspace for app in applications
        if app.window_class and any(c.get('mapped') and c.get('class') == app.window_class
                                    and c.get('workspace', {}).get('id') == app.workspace
                                    for c in clients)})
    if not open_workspaces:
        return 1
    step = 1 if action == 'next' else -1
    if current not in open_workspaces:
        return open_workspaces[0 if step > 0 else -1]
    return open_workspaces[(open_workspaces.index(current) + step) % len(open_workspaces)]
