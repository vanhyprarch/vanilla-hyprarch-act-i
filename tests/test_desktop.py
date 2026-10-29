# SPDX-License-Identifier: GPL-2.0-only
import unittest
from unittest.mock import Mock
from adapters.catalog import Application
from services.session.desktop import DesktopMonitor

APP = Application('jellyfin','Jellyfin','Media','org.example.Jellyfin',2,'jellyfin')
WINDOW = {'address':'0x123','class':'jellyfin','mapped':True,'workspace':{'id':2}}


class DesktopFocusTests(unittest.TestCase):
    def run_refresh(self, workspace, active, clients=None):
        hypr = Mock()
        data = {'activeworkspace':{'id':workspace}, 'clients':clients or [WINDOW], 'activewindow':active}
        hypr.query.side_effect = data.__getitem__
        callback = Mock()
        DesktopMonitor(hypr,[APP],callback).refresh()
        return hypr, callback

    def test_missing_player_focus_is_repaired_without_workspace_switch(self):
        hypr, callback = self.run_refresh(2,{})
        hypr.dispatch.assert_called_once_with('hl.dsp.focus({window="address:0x123"})')
        callback.assert_called_once_with(2)

    def test_window_recreation_keeps_same_workspace_policy(self):
        hypr, callback = self.run_refresh(2,{})
        callback.assert_called_once_with(2)
        self.assertNotIn('workspace=',hypr.dispatch.call_args.args[0])

    def test_home_does_not_activate_background_player(self):
        hypr, callback = self.run_refresh(1,{'address':'0xhome','workspace':{'id':1}})
        hypr.dispatch.assert_not_called()
        callback.assert_called_once_with(1)

    def test_valid_focused_dialog_is_not_overridden(self):
        hypr, _ = self.run_refresh(2,{'address':'0xdialog','workspace':{'id':2}})
        hypr.dispatch.assert_not_called()

    def test_stale_other_workspace_focus_is_repaired(self):
        hypr, _ = self.run_refresh(2,{'address':'0xhome','workspace':{'id':1}})
        hypr.dispatch.assert_called_once()
