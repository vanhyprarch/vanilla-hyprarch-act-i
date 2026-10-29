# SPDX-License-Identifier: GPL-2.0-only
"""Normal compositor window actions, independent of the application catalog."""
import json


def close_active_window(hyprland):
    window = hyprland.query('activewindow')
    workspace = window.get('workspace', {}).get('id')
    address = window.get('address')
    if not address or workspace == 1 or window.get('class') == 'org.quickshell':
        return False
    # Same graceful dispatcher as desktop Super+Q/W. Pin the inspected window
    # so an intervening focus change cannot close the Home or another app.
    selector = json.dumps('address:' + address)
    hyprland.dispatch('hl.dsp.window.close({window=' + selector + '})')
    hyprland.home_if_active(workspace)
    return True
