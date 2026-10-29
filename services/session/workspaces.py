# SPDX-License-Identifier: GPL-2.0-only
"""Workspace navigation never launches an application or sends it UI commands."""


def target_workspace(action, applications, clients, current):
    if action == 'home':
        return 1
    workspaces = [1] + sorted({app.workspace for app in applications
        if app.window_class and any(c.get('mapped') and c.get('class') == app.window_class
                                    and c.get('workspace', {}).get('id') == app.workspace
                                    for c in clients)})
    step = 1 if action == 'next' else -1
    if current not in workspaces:
        return workspaces[0 if step > 0 else -1]
    return workspaces[(workspaces.index(current) + step) % len(workspaces)]
